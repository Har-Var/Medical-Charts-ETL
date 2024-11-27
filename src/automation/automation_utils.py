import os
import time
from datetime import datetime
import re
import shutil
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .recon_report_update import update_header_and_detail_tables
from .slack_messages import send_slack_message, delete_all_messages
from utils import clear_folder
from dataprep import increment_charts
from .recon_report_load import (
    load_header_and_detail_to_sql,
    reset_process_sql_tables,
    auto_load_to_sql_tables,
)
from config import (
    rrl_staging,
    rrl_input,
    rrl_input_archive,
    rrl_log,
    rru_input,
    rru_input_archive,
    rru_log,
    active_vendor_list,
    report_base,
    recon_report_load_channel_id,
    recon_load_trigger,
    recon_report_update_channel_id,
    recon_update_trigger,
)


def ntimes_10percent_increment(n):
    """
    Increment charts n times by 10% each time, then update report tables.

    Parameters
    ----------
    n : int
        The number of times to increment charts by 10%.

    Returns
    -------
    None
    """
    for i in range(0, n):
        increment_charts()
    update_header_and_detail_tables()


def cleanup_automation_locs(process_name):
    """
    Cleaning up all automation process folders.

    Parameters
    ----------
    process_name : str
        The name of the process to clean up. Must be one of the following:
            - recon_report_load
            - recon_report_update

    Returns
    -------
    None
    """

    if process_name == "recon_report_load":
        clear_folder(rrl_input)
        clear_folder(rrl_input_archive)
        clear_folder(rrl_log)
    elif process_name == "recon_report_update":
        clear_folder(rru_input)
        clear_folder(rru_input_archive)
        clear_folder(rru_log)


def copy_reports_to_automation():
    """
    Copies all report files from each vendor's directory in the report base location
    to the automation staging area, excluding vendor chartlist files.

    This function clears the staging directory before copying the files. It
    iterates over each vendor directory in the report base, removes any files
    matching the vendor chartlist naming pattern, and then copies the remaining
    files to the staging directory.

    Global Variables
    ----------------
    active_vendor_list : list
        A list of active vendors whose chartlist files should be excluded.
    report_base : str
        The base directory where vendor report directories are located.
    rrl_staging : str
        The directory where the reports should be copied to.

    Returns
    -------
    None
    """
    global active_vendor_list, report_base, rrl_staging
    clear_folder(rrl_staging)
    remove_items = [f"{vendor}_chartlist.txt" for vendor in active_vendor_list]
    vendors = os.listdir(report_base)

    for vendor in vendors:
        vendor_report_loc = os.path.join(report_base, vendor)
        vendor_reports = os.listdir(vendor_report_loc)
        for item in remove_items:
            if item in vendor_reports:
                vendor_reports.remove(item)
        for file in vendor_reports:
            shutil.copy(os.path.join(vendor_report_loc, file), rrl_staging)


def configure_logging(file_name, timestamp, process_name):
    """
    Configures logging for a specific file and process, creating a logger and log file.

    Parameters
    ----------
    file_name : str
        The name of the file for which logging is being configured.
    timestamp : datetime
        The timestamp used to create a unique log file name.
    process_name : str
        The name of the process associated with the logging, either 'recon_report_load' or 'recon_report_update'.

    Returns
    -------
    tuple
        A tuple containing the logger object and the path to the log file.
    """
    # Generate a timestamp in the format YYYYMMDD_HHMMSS_fff
    timestamp_frmt = timestamp.strftime("%Y%m%d_%H%M%S_%f")[
        :-3
    ]  # Keep only 3 digits for milliseconds
    # Create the log file name using the process name and timestamp
    if process_name == "recon_report_load":
        log_loc = rrl_log
    elif process_name == "recon_report_update":
        log_loc = rru_log
    log_file = os.path.join(log_loc, f"{process_name}_{timestamp_frmt}.log")
    # Create a logger
    logger = logging.getLogger(file_name)
    logger.setLevel(logging.INFO)
    # Create file handler with the log file
    handler = logging.FileHandler(log_file)
    handler.setLevel(logging.INFO)
    # No formatting for plain text logs
    logger.addHandler(handler)
    return logger, log_file


def log_output_data(logger, process, data=None, status="Success"):
    """
    Logs the output data for the given process.

    Parameters
    ----------
    logger : logging.Logger
        The logger to use for logging the output data.
    process : str
        The name of the process, either 'recon_report_load' or 'recon_report_update'.
    data : dict, optional
        A dictionary containing the detailed information to log. If not provided, the
        log message will only contain the status and timestamp.
    status : str, optional
        The status of the process, either 'Success' or 'Error'. Defaults to 'Success'.
    """
    if process == "recon_report_load":
        # If the status is "Error", only log the status and skip the stats
        if status == "Error":
            log_message = (
                f"Status: {status}\n" f"TimeStamp: {time.strftime('%Y-%m-%d %H:%M:%S')}"
            )
        else:
            # For success, log the detailed information
            log_message = (
                f"Status: {status}\n"
                f"TimeStamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"ReportName: {data.get('ReportName', 'Unknown')}\n"
                f"ReportFileDate: {data.get('ReportFileDate', 'Unknown')}\n"
                f"Vendor: {data.get('Vendor', 'Unknown')}\n"
                f"FileCount: {data.get('FileCount', 'Unknown')}\n"
                f"UniqueCount: {data.get('UniqueCount', 'Unknown')}\n"
                f"FirstDelivery: {data.get('FirstDelivery', 'Unknown')}\n"
                f"LastDelivery: {data.get('LastDelivery', 'Unknown')}\n"
                "\n"
            )
    elif process == "recon_report_update":
        # If the status is "Error", only log the status and skip the stats
        if status == "Error":
            log_message = (
                f"Status: {status}\n" f"TimeStamp: {time.strftime('%Y-%m-%d %H:%M:%S')}"
            )
        else:
            # For success, log the detailed information
            log_message = (
                f"Status: {status}\n" f"TimeStamp: {time.strftime('%Y-%m-%d %H:%M:%S')}"
            )
    logger.info(log_message)


# Event Handler Class
class NewFileHandler(FileSystemEventHandler):
    def __init__(self, process_name, report_name_pattern):
        """
        Initialize a NewFileHandler object.

        Parameters
        ----------
        process_name : str
            The name of the process, either 'recon_report_load' or 'recon_report_update'.
        report_name_pattern : str
            The regular expression pattern to match the file name of the report.
        """
        self.process_name = process_name
        self.report_name_pattern = report_name_pattern

    def on_created(self, event):
        """
        Triggered when a new file is created in the monitoring location.

        Parameters
        ----------
        event : watchdog.events.FileCreatedEvent
            The event object containing information about the new file.

        Returns
        -------
        None

        Notes
        -----
        This function is called by the watchdog library when a new file is created
        in the monitoring location. It checks if the file name matches the naming
        convention for this process and logs the event. If the file name matches,
        it calls the process_file function to process the file, and logs the
        results. If an exception occurs during processing, it logs the error and
        sends an error message to Slack.
        """
        if event.is_directory:
            return
        file_name = os.path.basename(event.src_path)
        timestamp_base = datetime.now()
        # Check if the file name matches the naming convention for this process
        if re.match(self.report_name_pattern, file_name):
            timestamp_frmt = timestamp_base.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            # Configure logging for the new file with dynamic process name
            logger, log_file = configure_logging(
                file_name, timestamp_base, self.process_name
            )
            logger.info(f"New file detected: {file_name}")
            try:
                # Call the process_file function and process the file
                if self.process_name == "recon_report_load":
                    parsed_output = load_header_and_detail_to_sql(
                        file_name, process_name=self.process_name
                    )
                elif self.process_name == "recon_report_update":
                    print("Starting Recon Tables Update")
                    update_header_and_detail_tables()
                    parsed_output = None
                log_output_data(
                    logger,
                    process=self.process_name,
                    data=parsed_output,
                    status="Success",
                )
                # Send a success message
                send_slack_message(
                    processname=self.process_name,
                    filename=file_name,
                    timestamp=timestamp_frmt,
                    logfile_loc=log_file,
                    status="Success",
                )

            except Exception as e:
                log_output_data(logger, process=self.process_name, status="Error")
                logger.error(f"Error Details: {e}\n\n")
                # Send an error message
                send_slack_message(
                    processname=self.process_name,
                    filename=file_name,
                    timestamp=timestamp_frmt,
                    logfile_loc=log_file,
                    status="Error",
                    exception=e,
                )


# Function to start monitoring the folder for a specific process
def start_monitoring(monitoring_location, process_name, report_name_pattern):
    """
    Starts monitoring the specified folder for new files matching the given
    report name pattern. Calls the process_file function when a new file is
    detected.

    Parameters
    ----------
    monitoring_location : str
        The path to the folder to monitor for new files.
    process_name : str
        The name of the process, either 'recon_report_load' or 'recon_report_update'.
    report_name_pattern : str
        The regular expression pattern to match the file name of the report.

    Returns
    -------
    None
    """
    event_handler = NewFileHandler(process_name, report_name_pattern)
    observer = Observer()
    observer.schedule(event_handler, monitoring_location, recursive=False)
    print(
        f"Monitoring started on folder: {monitoring_location} for process: {process_name}"
    )
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def reset_and_monitor_rrl():
    """
    Resets and starts monitoring the recon_report_load process.

    This function clears and copies again the reports from the source to the
    automation staging area, deletes all messages from the Recon Report Load
    channel, cleans up the automation locations for the process, resets the
    Recon Report Load SQL tables and starts monitoring the folder for new
    reports.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    global rrl_input, recon_report_load_channel_id, recon_load_trigger
    print("Clearing Reports from Automation Staging, Copying again from Source")
    copy_reports_to_automation()
    print("Done")
    print("Deleting Messages from Recon Report Load Channel")
    delete_all_messages(recon_report_load_channel_id)
    print("Done")
    print("Cleaning up Automation Locs")
    cleanup_automation_locs(process_name="recon_report_load")
    print("Done")
    print("Resetting Recon Report Load SQL Tables")
    reset_process_sql_tables()
    print("Done")
    print("Starting Recon Report Load Monitoring")
    start_monitoring(
        rrl_input,
        process_name="recon_report_load",
        report_name_pattern=recon_load_trigger,
    )


def reset_and_process_rrl():
    """
    Resets and processes the recon_report_load process.

    This function clears and copies again the reports from the source to the
    automation staging area, cleans up the automation locations for the process,
    resets the Recon Report Load SQL tables and auto loads the reports to the
    SQL tables.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """

    print("Clearing Reports from Automation Staging, Copying again from Source")
    copy_reports_to_automation()
    print("Done")
    print("Cleaning up Automation Locs")
    cleanup_automation_locs(process_name="recon_report_load")
    print("Done")
    print("Resetting Recon Report Load SQL Tables")
    reset_process_sql_tables()
    print("Done")
    print("Auto Sequentially Loading Reports to SQL Tables")
    auto_load_to_sql_tables(process_name="recon_report_load")
    print("Done")


def reset_and_monitor_rru():
    """
    Resets and starts monitoring the recon_report_update process.

    This function deletes all messages from the Recon Report Update channel, cleans up the
    automation locations for the process and starts monitoring the specified folder for
    new files matching the given report name pattern.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """

    global rru_input, recon_report_update_channel_id, recon_update_trigger
    print("Deleting Messages from Recon Report Update Channel")
    delete_all_messages(recon_report_update_channel_id)
    print("Done")
    print("Cleaning up Automation Locs")
    cleanup_automation_locs(process_name="recon_report_update")
    print("Done")
    print("Starting Recon Report Update Monitoring")
    start_monitoring(
        rru_input,
        process_name="recon_report_update",
        report_name_pattern=recon_update_trigger,
    )

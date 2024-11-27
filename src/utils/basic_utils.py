import os
import shutil
from pathlib import Path
from config import (
    automation_base_loc,
    rrl_loc,
    rru_loc,
    rrl_staging,
    rrl_input,
    rrl_input_archive,
    rrl_log,
    rru_staging,
    rru_input,
    rru_input_archive,
    rru_log,
    data_base_location,
    report_base,
    charts_base,
    resource_loc,
    charts_drop_off_location,
    payment_reconciliation_location,
    excel_setup_location,
    excel_filepath,
)


def clear_folder(location):
    """
    Clears the given folder location by removing all files and subfolders.

    Parameters
    ----------
    location : str
        The path to the folder to clear.

    Returns
    -------
    None
    """
    for item in os.listdir(location):
        item_path = os.path.join(location, item)
        if os.path.isdir(item_path):
            # Remove the folder and its contents
            shutil.rmtree(item_path)
        elif os.path.isfile(item_path):
            # Remove the file
            os.remove(item_path)


def loc_variable_fetch(process_name):
    """
    Fetches the location variables based on the given process_name.

    Parameters
    ----------
    process_name : str
        The name of the process, either 'recon_report_load' or 'recon_report_update'.

    Returns
    -------
    A tuple of four strings: staging location, input location, input archive location and log location.
    """

    if process_name == "recon_report_load":
        staging_loc = rrl_staging
        input_loc = rrl_input
        input_archive_loc = rrl_input_archive
        log_loc = rrl_log
    elif process_name == "recon_report_update":
        staging_loc = rru_staging
        input_loc = rru_input
        input_archive_loc = rru_input_archive
        log_loc = rru_log
    return staging_loc, input_loc, input_archive_loc, log_loc


def open_excelsetup_file():
    """
    Opens the Excel setup file in Excel.

    The Excel setup file contains the macros to export payment reconciliation reports files.
    This function opens the file in Excel for editing.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    filepath = excel_filepath
    os.system(f'start EXCEL.EXE "{filepath}"')


def ensure_directories_exist(*directories):
    """
    Ensures that all directories given as arguments exist, and creates them if not.

    Parameters
    ----------
    *directories : str
        A variable number of arguments, each of which is a directory path.

    Returns
    -------
    None
    """
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)


def ensuring_project_directories_all_exist():
    """
    Ensures that all necessary project directories exist.

    This function checks for the existence of multiple project directories
    required for various automation processes and report management. If any
    of the specified directories do not exist, they are created.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    ensure_directories_exist(
        automation_base_loc,
        rrl_loc,
        rru_loc,
        rrl_staging,
        rrl_input,
        rrl_input_archive,
        rrl_log,
        rru_staging,
        rru_input,
        rru_input_archive,
        rru_log,
        data_base_location,
        report_base,
        charts_base,
        resource_loc,
        charts_drop_off_location,
        payment_reconciliation_location,
        excel_setup_location,
    )


def clean_leaf_directories():
    """
    Deletes all files and subdirectories from all last level directories in the project.
    Leaves out automation>trigger directory since it contains trigger file which needs to be shared

    This function is used to clean up the project directories before starting a new
    execution of the automation processes.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    clear_folder(rrl_input)
    clear_folder(rrl_input_archive)
    clear_folder(rrl_log)
    clear_folder(rrl_staging)
    clear_folder(rru_input)
    clear_folder(rru_input_archive)
    clear_folder(rru_log)
    clear_folder(report_base)
    clear_folder(charts_base)

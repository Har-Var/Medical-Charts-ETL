import os
import shutil
import pyodbc
import re
from datetime import datetime
from utils import loc_variable_fetch, clear_folder
from config import conn_str


# Function to convert to SQL Server datetime format (UTC)
def to_sql_server_format(date_str):
    """
    Converts a date string from the format 'YYYYMMDDTHHMMSSZ' to SQL Server datetime format.

    Parameters
    ----------
    date_str : str
        The date string in the format 'YYYYMMDDTHHMMSSZ'.

    Returns
    -------
    str
        The formatted date string in SQL Server datetime format 'YYYY-MM-DD HH:MM:SS'.
    """
    return datetime.strptime(date_str, "%Y%m%dT%H%M%SZ").strftime("%Y-%m-%d %H:%M:%S")


def parse_reports(current_file):
    """
    Parses a given report file to extract relevant data including report name, 
    date, vendor, file count, first and last delivery times, and chart details.

    Parameters
    ----------
    current_file : str
        The name of the report file to be parsed.

    Returns
    -------
    dict
        A dictionary containing extracted data:
        - "ReportFileDate": str, the report file date in 'YYYY-MM-DD' format.
        - "ReportName": str, the name of the report file.
        - "Vendor": str, the vendor name extracted from the report name.
        - "FileCount": int, the total number of charts delivered as mentioned in the report.
        - "FirstDelivery": str, the first chart delivery timestamp in SQL Server format.
        - "LastDelivery": str, the last chart delivery timestamp in SQL Server format.
        - "ChartListWithDupes": list, list of chart names with potential duplicates.
        - "ChartList": list, list of unique chart names.
        - "UniqueCount": int, the count of unique charts delivered.
    """
    input_loc = loc_variable_fetch("recon_report_load")[1]
    file_path = os.path.join(input_loc, current_file)
    # Read the file content
    with open(file_path, "r") as file:
        data = file.read()
    # Extract ReportName
    report_name = current_file
    # Extract ReportFileDate
    report_file_date = re.search(r"_([^_]+)\.txt$", report_name).group(1)
    report_file_date_sql_format = datetime.strptime(
        report_file_date, "%Y%m%d"
    ).strftime("%Y-%m-%d")
    # Extract Vendor
    vendor = report_name.split("_")[0]
    # Extract FileCount
    file_count = int(re.search(r"Charts Delivered:\s+(\d+)", data).group(1))
    # Extract FirstDelivery
    first_delivery = re.search(r"First Chart Delivered at:\s+(\d+T\d+Z)", data).group(1)
    first_delivery_sql_format = to_sql_server_format(first_delivery)
    # Extract LastDelivery
    last_delivery = re.search(r"Last Chart Delivered at:\s+(\d+T\d+Z)", data).group(1)
    last_delivery_sql_format = to_sql_server_format(last_delivery)
    # Extract chartlist
    chartlist_with_dupes = re.findall(r"\d+T\d+Z_\w+\.json", data)
    chartlist = list(set(chartlist_with_dupes))
    # Get UniqueCount
    unique_count = len(chartlist)

    # Output
    output = {
        "ReportFileDate": report_file_date_sql_format,
        "ReportName": report_name,
        "Vendor": vendor,
        "FileCount": file_count,
        "FirstDelivery": first_delivery_sql_format,
        "LastDelivery": last_delivery_sql_format,
        "ChartListWithDupes": chartlist_with_dupes,
        "ChartList": chartlist,
        "UniqueCount": unique_count,
    }

    return output


def header_sql_push(output):
    """
    Inserts the report header data into the SQL Server `report_recon_header` table.

    Parameters
    ----------
    output : dict
        A dictionary containing the report header data.
    """

    global conn_str
    # Connect to SQL Server
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # Define the SQL INSERT query
    insert_query = """
        INSERT INTO common.report_recon_header (
            report_push_date, report_file_date, report_name, vendor, file_count, 
            unique_count, first_delivery, last_delivery
        )
        VALUES (CONVERT(date, GETUTCDATE()), ?, ?, ?, ?, ?, ?, ?)
    """

    # Data to insert
    data_to_insert = (
        output["ReportFileDate"],  # report_file_date
        output["ReportName"],  # report_name
        output["Vendor"],  # vendor
        output["FileCount"],  # file_count
        output["UniqueCount"],  # unique_count
        output["FirstDelivery"],  # first_delivery
        output["LastDelivery"],  # last_delivery
    )

    # Execute the insert query
    cursor.execute(insert_query, data_to_insert)
    # Commit the transaction
    conn.commit()
    # Close the connection
    cursor.close()
    conn.close()


def detail_sql_push(output):
    """
    Inserts the report detail data into the SQL Server `report_recon_detail` table.

    Parameters
    ----------
    output : dict
        A dictionary containing the report detail data.
    """
    
    global conn_str

    # Connect to SQL Server
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # Step 1: Retrieve the last inserted header ID from the `report_recon_header` table
    cursor.execute("SELECT TOP 1 id FROM common.report_recon_header ORDER BY id DESC")
    header_id = cursor.fetchone()[0]  # Get the last inserted header ID

    # Step 2: Insert each chart from the chartlist into the `report_recon_detail` table
    insert_query = """
        INSERT INTO common.report_recon_detail (
            header_id, chart_name, insert_datetime, update_datetime, report_name
        )
        VALUES (?, ?, GETUTCDATE(), GETUTCDATE(), ?)
    """

    # Step 3: Loop through the chartlist and insert each chart
    for chart in output["ChartList"]:
        data_to_insert = (
            header_id,  # header_id (from the header table)
            chart,  # chart_name (from the chartlist)
            output["ReportName"],  # report_name (same as in the header)
        )

        cursor.execute(insert_query, data_to_insert)

    # Commit the transaction
    conn.commit()

    # Close the connection
    cursor.close()
    conn.close()


def sort_by_date(filename):
    """Extracts the date from a filename and returns it as an integer."""
    match = re.search(r"(\d{8})", filename)
    return int(match.group(1))


def load_header_and_detail_to_sql(file, process_name):
    """
    Loads the header and detail data from a given report file into SQL Server.

    Parameters
    ----------
    file : str
        The name of the report file to load.
    process_name : str
        The name of the process, either 'recon_report_load' or 'recon_report_update'.
    """
    
    parsed_output = parse_reports(file)
    header_sql_push(parsed_output)
    detail_sql_push(parsed_output)
    # Moving File from Input to Input archive
    input_loc = loc_variable_fetch(process_name)[1]
    input_archive_loc = loc_variable_fetch(process_name)[2]
    shutil.move(os.path.join(input_loc, file), input_archive_loc)
    return parsed_output


def auto_load_to_sql_tables(process_name):
    """
    Automatically loads all report files from the staging area to the SQL Server database.

    Parameters
    ----------
    process_name : str
        The name of the process, either 'recon_report_load' or 'recon_report_update'.
    """
    
    staging_loc = loc_variable_fetch(process_name)[0]
    input_loc = loc_variable_fetch(process_name)[1]
    input_archive_loc = loc_variable_fetch(process_name)[2]
    all_files = os.listdir(staging_loc)
    # Sort the list using the custom sorting function
    sorted_all_files = sorted(all_files, key=sort_by_date)
    for file in sorted_all_files:
        # Copying file from staging to input
        shutil.copy(os.path.join(staging_loc, file), input_loc)
        load_header_and_detail_to_sql(file, process_name)
    clear_folder(input_archive_loc)


def reset_process_sql_tables():
    """
    Resets the SQL Server tables used by the Recon Report Load process.

    Resets the `report_recon_header` and `report_recon_detail` tables by deleting all
    rows and reseeding the identity columns.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """

    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # Define the SQL INSERT query
    delete_reseed_query = """
        DELETE FROM common.report_recon_header;
    DBCC CHECKIDENT ('common.report_recon_header', RESEED, 0);
        DELETE FROM common.report_recon_detail;
    DBCC CHECKIDENT ('common.report_recon_detail', RESEED, 0);
    """

    # Execute the insert query
    cursor.execute(delete_reseed_query)
    # Commit the transaction
    conn.commit()
    # Close the connection
    cursor.close()
    conn.close()

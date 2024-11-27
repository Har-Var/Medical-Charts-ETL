import os
import pyodbc
import random
from utils import clear_folder
from config import (
    report_base,
    charts_drop_off_location,
    conn_str,
    active_vendor_list,
)


# Common Utility Functions
def retain_random_charts(chartlist):
    """
    Takes a list of charts and returns a new list with a randomly selected
    subset of charts, with the size of the subset being 60% of the original
    list. The original list is shuffled before selecting the subset.

    Parameters
    ----------
    chartlist : list
        A list of charts

    Returns
    -------
    list
        A new list with a randomly selected subset of charts
    """
    random.shuffle(chartlist)
    total_charts_count = len(chartlist)
    # Getting only 60% of the charts
    limited_charts_count = int(0.6 * total_charts_count)
    limited_charts = chartlist[:limited_charts_count]
    return limited_charts


def print_chartlists_summary(all_vendors_data):
    """
    Prints a summary of the charts for each vendor. The summary includes the
    number of charts in each type (e.g. Windows, CSV, SQL) and the total number
    of charts for each vendor.

    Parameters
    ----------
    all_vendors_data : dict
        A dictionary containing the charts for each vendor. The structure of
        the dictionary is as follows:
        {
            'vendor_name': {
                'chart_type': [chart1, chart2, ...],
                ...
            },
            ...
        }
    """
    for vendor in all_vendors_data:
        print(f"{vendor} :- ")
        for chart_type, chart_list in all_vendors_data[vendor].items():
            print(f"{chart_type} : {len(chart_list)}")
        print()


def clear_sql_table_and_insert(cursor, vendor, table_name, data_list):
    """
    Deletes all records from the specified table in the specified vendor's
    database, and then inserts the records from the provided list into the
    table.

    Parameters
    ----------
    cursor : pyodbc.Cursor
        A cursor object connected to a SQL Server database.
    vendor : str
        The name of the vendor.
    table_name : str
        The name of the table to delete and insert records into.
    data_list : list
        A list of chart names to be inserted into the table.
    """
    delete_query = f"DELETE FROM {vendor}.{table_name}"
    cursor.execute(delete_query)

    # Insert new records into the table
    insert_query = f"INSERT INTO {vendor}.{table_name} (chartname) VALUES (?)"
    for chartname in data_list:
        cursor.execute(insert_query, chartname)


def get_and_push_charts_tosql(active_vendor):
    """
    Retrieves a list of chart names from a file in the specified vendor's directory,
    randomly selects a subset of charts (60% of total), and then deletes all records
    from the specified table in the specified vendor's database and inserts the
    selected records into the table.

    Parameters
    ----------
    active_vendor : str
        The name of the vendor.

    Returns
    -------
    dict
        A dictionary containing three lists: "All Charts", "Limited Charts", and
        "Left Charts", corresponding to the full list of charts, the selected subset
        of charts, and the remaining charts that were not selected, respectively.
    """
    global table_name, report_base
    report_location = os.path.join(report_base, active_vendor)
    chartlist_name = f"{active_vendor}_chartlist.txt"
    chartlist_location = os.path.join(report_location, chartlist_name)

    chartlist_file = open(chartlist_location, "r")
    data = chartlist_file.read()
    data_into_list = data.split("\n")
    chartlist_file.close()

    full_list = data_into_list.copy()
    limited_list = retain_random_charts(data_into_list)
    left_list = set(full_list) - set(limited_list)

    # Connect to SQL Server
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # Perform the delete and insert operations for both tables
    clear_sql_table_and_insert(cursor, active_vendor, "chartlookup", limited_list)
    clear_sql_table_and_insert(cursor, active_vendor, "leftcharts", left_list)

    # Commit the transaction
    conn.commit()

    # Close the connection
    cursor.close()
    conn.close()
    lists_dict = {
        "All Charts": full_list,
        "Limited Charts": limited_list,
        "Left Charts": left_list,
    }
    return lists_dict


def push_all_sql_charts():
    """
    Pushes all charts from the report base location to the SQL Server database.

    This function iterates over all active vendors, retrieves their charts from the
    report base location, randomly selects a subset of charts (60% of total), and
    then deletes all records from the chartlookup and leftcharts tables in the
    specified vendor's database and inserts the selected records into the tables.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    global active_vendor_list
    all_charts = {}

    for vendor in active_vendor_list:
        charts = get_and_push_charts_tosql(active_vendor=vendor)
        all_charts[vendor] = charts
    print_chartlists_summary(all_charts)


def get_and_create_windows_charts(active_vendor):
    """
    Retrieves a list of chart names from a file in the specified vendor's directory,
    randomly selects a subset of charts (60% of total), creates empty JSON files
    for the selected charts in the vendor's drop-off location, and saves the
    remaining charts to a separate file.

    Parameters
    ----------
    active_vendor : str
        The name of the vendor.

    Returns
    -------
    dict
        A dictionary containing three lists: "All Charts", "Limited Charts", and
        "Left Charts", corresponding to the full list of charts, the selected subset
        of charts, and the remaining charts that were not selected, respectively.
    """
    report_location = os.path.join(report_base, active_vendor)
    chartlist_name = f"{active_vendor}_chartlist.txt"
    chartlist_location = os.path.join(report_location, chartlist_name)
    vendor_charts_drop_off_location = os.path.join(
        charts_drop_off_location, active_vendor
    )

    chartlist_file = open(chartlist_location, "r")
    data = chartlist_file.read()
    data_into_list = data.split("\n")
    chartlist_file.close()

    full_list = data_into_list.copy()
    limited_list = retain_random_charts(data_into_list)
    left_list = set(full_list) - set(limited_list)

    # Ensure the output folder exists
    if not os.path.exists(vendor_charts_drop_off_location):
        os.makedirs(vendor_charts_drop_off_location)

    # Create empty JSON files
    for filename in limited_list:
        file_path = os.path.join(vendor_charts_drop_off_location, filename)
        # Create empty JSON files
        with open(file_path, "w") as f:
            pass  # This will create an empty file

    # Saving all left charts in a combined file
    leftcharts_name = f"{active_vendor}_left_charts.txt"
    leftcharts_location = os.path.join(vendor_charts_drop_off_location, leftcharts_name)

    with open(leftcharts_location, "w") as f:
        for i, chart in enumerate(left_list):
            if i < len(left_list) - 1:
                f.write(f"{chart}\n")
            else:
                f.write(f"{chart}")
    lists_dict = {
        "All Charts": full_list,
        "Limited Charts": limited_list,
        "Left Charts": left_list,
    }
    return lists_dict


def create_all_windows_charts():
    """
    Creates empty JSON files for all charts from all active vendors in the windows
    drop-off location.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    global active_vendor_list
    clear_folder(charts_drop_off_location)
    all_charts = {}

    for vendor in active_vendor_list:
        charts = get_and_create_windows_charts(active_vendor=vendor)
        all_charts[vendor] = charts
    print_chartlists_summary(all_charts)

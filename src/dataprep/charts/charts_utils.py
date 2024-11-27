import os
import pyodbc
import json
from pprint import pprint
from utils import fetch_query
from config import (
    conn_str,
    report_base,
    charts_drop_off_location as windows_location,
    payment_reconciliation_location as csv_location,
    active_vendor_list,
    resource_loc,
)


def get_vendor_lists_stats(cursor, active_vendor):
    """
    Retrieves and returns the number of charts in each location for the given vendor.

    Parameters
    ----------
    cursor : pyodbc.Cursor
        An open cursor object connected to the database.
    active_vendor : str
        The name of the vendor.

    Returns
    -------
    dict
        A dictionary with 6 keys: "Report", "Windows", "CSV", "SQL", "Windows Left", "CSV Left", "SQL Left",
        each containing the number of charts in the respective location.
    """
    vendor_report_location = os.path.join(report_base, active_vendor)
    report_full_list = (
        open(
            os.path.join(vendor_report_location, f"{active_vendor}_chartlist.txt"), "r"
        )
        .read()
        .splitlines()
    )

    vendor_windows_location = os.path.join(windows_location, active_vendor)
    windows_location_charts = os.listdir(vendor_windows_location)
    windows_location_charts.remove(f"{active_vendor}_left_charts.txt")
    windows_location_left_charts = (
        open(
            os.path.join(vendor_windows_location, f"{active_vendor}_left_charts.txt"),
            "r",
        )
        .read()
        .splitlines()
    )

    vendor_csv_location = os.path.join(csv_location, active_vendor)
    csv_location_charts = (
        open(
            os.path.join(
                vendor_csv_location, f"{active_vendor}_charts_reconciliation.csv"
            ),
            "r",
        )
        .read()
        .splitlines()[1:]
    )
    csv_location_left_charts = (
        open(os.path.join(vendor_csv_location, f"{active_vendor}_leftcharts.csv"), "r")
        .read()
        .splitlines()[1:]
    )

    sql_location_charts = fetch_query(cursor, active_vendor, "chartlookup")
    sql_location_left_charts = fetch_query(cursor, active_vendor, "leftcharts")

    lists_dict = {
        "Report": len(report_full_list),
        "Windows": len(windows_location_charts),
        "CSV": len(csv_location_charts),
        "SQL": len(sql_location_charts),
        "Windows Left": len(windows_location_left_charts),
        "CSV Left": len(csv_location_left_charts),
        "SQL Left": len(sql_location_left_charts),
    }
    return lists_dict


def get_print_vendor_lists_stats():
    """
    Prints the statistics of charts for all active vendors.

    This function connects to the SQL Server database, retrieves the number
    of charts in various locations (report, Windows, CSV, SQL, and their
    respective left charts) for each vendor using the
    get_vendor_lists_stats function, and prints the results.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    for vendor in active_vendor_list:
        print(vendor)
        pprint(get_vendor_lists_stats(cursor, vendor), sort_dicts=False)
        print()
    # Close the connection
    cursor.close()
    conn.close()


def get_and_save_batch_size():
    """
    Saves the sample size for each vendor to a JSON file.

    This function counts the charts in the leftcharts.csv file for each vendor
    and calculates 10% of the total charts as the sample size. It then saves the
    counts and sample sizes to a JSON file named "chart_increment_sample_size.json"
    in the resource location.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    left_sizes = {}

    for active_vendor in active_vendor_list:
        # Construct the path to the vendor's CSV file
        vendor_csv_location = os.path.join(csv_location, active_vendor)

        # Read the leftcharts file and count the charts, skipping the header
        with open(
            os.path.join(vendor_csv_location, f"{active_vendor}_leftcharts.csv"), "r"
        ) as f:
            left_charts_count = len(f.read().splitlines()[1:])

        # Calculate the sample size (10% of the total charts)
        sample_size = left_charts_count // 10

        # Add a nested dictionary for each vendor with counts and sample size
        left_sizes[active_vendor] = {"Left": left_charts_count, "Sample": sample_size}

    # Save the data to a JSON file
    json_file_path = os.path.join(resource_loc, "chart_increment_sample_size.json")
    with open(json_file_path, "w") as json_file:
        json.dump(left_sizes, json_file, indent=4)
    get_print_vendor_lists_stats()

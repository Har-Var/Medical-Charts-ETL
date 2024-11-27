import os
import pyodbc
from utils import clear_folder, execute_stored_procedure
from config import (
    charts_drop_off_location as windows_location,
    payment_reconciliation_location as csv_location,
    active_vendor_list,
    conn_str,
    rru_input,
)


def get_charts_windows_and_csv(active_vendor):
    """
    Get charts from both windows and csv location.

    Parameters
    ----------
    active_vendor : str
        The name of the vendor.

    Returns
    -------
    tuple
        A tuple of two lists. The first contains charts from windows location, the
        second contains charts from csv location.
    """
    vendor_windows_location = os.path.join(windows_location, active_vendor)
    windows_location_charts = os.listdir(vendor_windows_location)
    windows_location_charts.remove(f"{active_vendor}_left_charts.txt")

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

    return windows_location_charts, csv_location_charts


def get_location_charts():
    """
    Aggregates charts from both Windows and CSV locations for all active vendors.

    This function iterates over all active vendors and retrieves their charts
    from both Windows and CSV locations by calling the get_charts_windows_and_csv
    function. It combines the charts from all vendors into two lists: one for
    Windows location charts and another for CSV location charts.

    Returns
    -------
    tuple
        A tuple containing two lists: the first list contains charts from
        the Windows location, and the second list contains charts from the
        CSV location.
    """
    global active_vendor_list
    windows_charts = []
    csv_charts = []
    for vendor in active_vendor_list:
        vendor_windows_charts, vendor_csv_charts = get_charts_windows_and_csv(
            active_vendor=vendor
        )
        windows_charts.extend(vendor_windows_charts)
        csv_charts.extend(vendor_csv_charts)
    return windows_charts, csv_charts


def create_temp_table_and_insert_charts(cursor, chartlist):
    """
    Creates a temporary table and inserts a list of chart names into it in batches.

    This function is used to create a temporary table and insert a list of chart names
    into it in batches. This allows us to avoid having to insert the full list of charts
    at once, which could be slow.

    Parameters
    ----------
    cursor : pyodbc.Cursor
        A cursor object connected to a SQL Server database.
    chartlist : list
        A list of chart names to be inserted into the temporary table.

    Returns
    -------
    None
    """
    cursor.execute(
        "IF OBJECT_ID('tempdb..#TempCharts') IS NOT NULL DROP TABLE #TempCharts"
    )
    cursor.execute(
        """
        CREATE TABLE #TempCharts (chart_name NVARCHAR(255))
    """
    )

    # Insert chart names into the temporary table in batches
    batch_size = 1000
    for i in range(0, len(chartlist), batch_size):
        batch = chartlist[i : i + batch_size]
        placeholders = ",".join("(?)" for _ in batch)
        insert_query = f"INSERT INTO #TempCharts (chart_name) VALUES {placeholders}"
        cursor.execute(insert_query, batch)


def update_using_temp_table(cursor, indicator):
    # Perform the update using a JOIN with the temporary table
    """
    Updates the specified indicator in the common.report_recon_detail table
    using a JOIN with a temporary table of chart names.

    Parameters
    ----------
    cursor : pyodbc.Cursor
        A cursor object connected to a SQL Server database.
    indicator : str
        The name of the indicator to be updated.

    Returns
    -------
    None
    """
    update_query = f"""
        UPDATE common.report_recon_detail
        SET {indicator} = 1, update_datetime = GETUTCDATE()
        FROM common.report_recon_detail r
        INNER JOIN #TempCharts t ON r.chart_name = t.chart_name
        where (r.exclusion_ind = 0 or r.exclusion_ind is NULL) 
		and (r.{indicator} = 0 or r.{indicator} is NULL)
    """
    cursor.execute(update_query)


def update_windows_and_csv_indicators(windows_charts, csv_charts):
    """
    Updates the drop_off_ind and payment_recon_ind indicators in the
    common.report_recon_detail table using two lists of chart names.

    Parameters
    ----------
    windows_charts : list
        A list of chart names for Windows charts.
    csv_charts : list
        A list of chart names for CSV charts.

    Returns
    -------
    None
    """
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # Insert Windows charts into a temp table and update
    create_temp_table_and_insert_charts(cursor, windows_charts)
    update_using_temp_table(cursor, "drop_off_ind")

    # Insert CSV charts into a temp table and update
    create_temp_table_and_insert_charts(cursor, csv_charts)
    update_using_temp_table(cursor, "payment_recon_ind")

    # Commit the transaction
    conn.commit()

    # Close the connection
    cursor.close()
    conn.close()


def update_header_and_detail_tables():
    """
    Updates the header and detail tables in the SQL Server database.

    This function first clears the input folder, then retrieves lists of charts
    from the Windows and CSV locations. It then updates the drop_off_ind and
    payment_recon_ind indicators in the common.report_recon_detail table using
    the lists of charts. Finally, it calls three stored procedures to update
    the common.chart_lookup table, the exclusion indicator in the
    common.report_recon_detail table, and the tally counts in the
    common.report_recon_header table.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    clear_folder(rru_input)
    windows_charts, csv_charts = get_location_charts()
    update_windows_and_csv_indicators(windows_charts, csv_charts)
    execute_stored_procedure(procedure_name="common.sp_update_chart_lookup_indicator")
    execute_stored_procedure(procedure_name="common.sp_update_exclusion_indicator")
    execute_stored_procedure(procedure_name="common.sp_update_header_tally_counts")

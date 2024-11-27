import datetime
import random
import os
from utils import clear_folder
from config import (
    report_base,
    datetime_format,
    date_format,
    time_format,
    time_start,
    time_stop,
    date_range_start,
    date_range_end,
    health_systems_list,
    min_chart,
    max_chart,
    mem_id_start,
    mem_id_end,
    active_vendor_list,
)


def generate_member_list(memid_start, memid_end):
    """
    Generates a list of member IDs in the format "MBRxxxxx" where xxxxx is a zero-padded
    five-digit number ranging from memid_start to memid_end (inclusive).

    Parameters
    ----------
    memid_start : int
        Starting member ID number.
    memid_end : int
        Ending member ID number.

    Returns
    -------
    None
    """

    global member_list
    member_list = []
    for i in range(memid_start, memid_end + 1):
        member_id = f"MBR{i:05d}"
        member_list.append(member_id)


def create_chartlist(start_dttm, end_dttm, total_report_chart, active_vendor):
    """
    Generates a list of chart names and their corresponding timestamps.

    This function creates a list of chart names based on the specified start
    and end datetime range, total number of charts, and active vendor. Each
    chart name is generated with a random timestamp within the given time
    range, a randomly selected member ID, and a randomly selected health
    system associated with the active vendor. The resulting chart names are
    in the format: '<timestamp>_<member>_<health_system>.json'.

    Parameters
    ----------
    start_dttm : datetime
        The starting datetime for the chart timestamps.
    end_dttm : datetime
        The ending datetime for the chart timestamps.
    total_report_chart : int
        The total number of charts to generate.
    active_vendor : str
        The name of the active vendor for which the charts are being generated.

    Returns
    -------
    tuple
        A tuple containing two lists:
        - List of generated chart names.
        - List of corresponding chart timestamps as datetime objects.
    """
    global member_list, health_systems_list, datetime_format
    time_difference = (end_dttm - start_dttm).total_seconds()
    created_chartlist = []
    all_timestamps = []

    select_health_systems = health_systems_list[active_vendor]

    for i in range(total_report_chart):
        random_seconds = random.uniform(0, time_difference)
        chart_datetime = start_dttm + datetime.timedelta(seconds=random_seconds)
        chart_timestamp = chart_datetime.strftime(datetime_format)
        chart_member = random.choice(member_list)
        chart_health_system = random.choice(select_health_systems)
        chart_name = (
            chart_timestamp + "_" + chart_member + "_" + chart_health_system + ".json"
        )
        created_chartlist.append(chart_name)
        all_timestamps.append(chart_datetime)
    return created_chartlist, all_timestamps


def create_content_base(
    report_dt_range, chart_no, dt_actual_start, dt_actual_end, chartlist
):
    """
    Generates the content of a report file given the report date range, total charts, actual start and end timestamps, and a list of chart names.

    Parameters
    ----------
    report_dt_range : str
        The date range of the report in 'YYYY-MM-DD to YYYY-MM-DD' format.
    chart_no : int
        The total number of charts delivered.
    dt_actual_start : str
        The actual start timestamp of the first chart delivered in 'YYYY-MM-DD HH:MM:SS' format.
    dt_actual_end : str
        The actual end timestamp of the last chart delivered in 'YYYY-MM-DD HH:MM:SS' format.
    chartlist : list
        A list of chart names.

    Returns
    -------
    str
        The content of the report file as a string.
    """
    chartlist_str = "\n".join(chartlist)

    content_base = f"""Delivery Report for {report_dt_range} 

Charts Delivered: {chart_no}	

First Chart Delivered at: {dt_actual_start}
Last Chart Delivered at: {dt_actual_end}

{chartlist_str}
"""
    return content_base


def create_duplicate_charts(charts, chartno):
    """
    Creates a list of charts with duplicates.

    Given a list of chart names and the total number of charts, this function
    generates a new list with duplicates. The number of duplicates is calculated
    by taking a value between 0 and 0.15 of the total number of charts and
    applying a skewed distribution to it. The resulting list is then returned.

    Parameters
    ----------
    charts : list
        The list of chart names.
    chartno : int
        The total number of charts.

    Returns
    -------
    list
        The list of chart names with duplicates.
    """
    maxdups = int(chartno * 0.15)
    rand_no = random.uniform(0, 1)
    skewed_value = rand_no**2.5
    actual_dups = int(skewed_value * maxdups)
    for dup in range(actual_dups):
        charts.append(random.choice(charts))
    return charts


def create_report_content(report_date, active_vendor):
    """
    Generates a report content given the report date and active vendor.

    This function generates a list of chart names and timestamps for the given
    report date and active vendor. The total number of charts is chosen randomly
    between the minimum and maximum limits. The start and end times of the report
    are also randomly chosen between the minimum and maximum limits. The resulting
    chart names and timestamps are then used to create a report content string
    and a list of chart names.

    Parameters
    ----------
    report_date : datetime
        The date of the report.
    active_vendor : str
        The name of the active vendor.

    Returns
    -------
    tuple
        A tuple containing the report content string and the list of chart names.
    """
    global min_chart, max_chart, time_start, time_stop, datetime_format, time_format
    report_start_time = datetime.datetime.strptime(time_start, time_format).time()
    report_stop_time = datetime.datetime.strptime(time_stop, time_format).time()
    report_day_start = report_date - datetime.timedelta(days=1)
    report_day_end = report_date
    report_chart_no = random.randint(min_chart, max_chart)
    report_valid_dt_start = datetime.datetime.combine(
        report_day_start, report_start_time
    )
    report_valid_dt_end = datetime.datetime.combine(report_day_end, report_stop_time)
    report_chartlist, report_chart_timestamps = create_chartlist(
        report_valid_dt_start, report_valid_dt_end, report_chart_no, active_vendor
    )
    for_dup_report_chartlist = report_chartlist.copy()
    final_report_chartlist = create_duplicate_charts(
        for_dup_report_chartlist, report_chart_no
    )
    final_report_chart_no = len(final_report_chartlist)
    first_chart_dt = min(report_chart_timestamps).strftime(datetime_format)
    last_chart_dt = max(report_chart_timestamps).strftime(datetime_format)
    report_date_range = f"{report_day_start.strftime(date_format)}{time_start} to {report_day_end.strftime(date_format)}{time_stop}"
    report_content = create_content_base(
        report_date_range,
        final_report_chart_no,
        first_chart_dt,
        last_chart_dt,
        final_report_chartlist,
    )
    return report_content, report_chartlist


def generate_files(active_vendor):
    """
    Generates daily reports and saves them to the specified report base location.

    Parameters
    ----------
    active_vendor : str
        The name of the active vendor.

    Returns
    -------
    None
    """
    global date_range_start, date_range_end, date_format, report_base
    output_location = os.path.join(report_base, active_vendor)
    all_charts = []
    current_date = date_range_start
    while current_date <= date_range_end:
        report_date = current_date.strftime(date_format)
        report_name = f"{active_vendor}_daily_report_{report_date}.txt"
        report_content, report_charts = create_report_content(
            current_date, active_vendor
        )
        all_charts.extend(report_charts)
        if not os.path.exists(output_location):
            os.makedirs(output_location)
        report_location = os.path.join(output_location, report_name)
        with open(report_location, "w") as f:
            f.write(report_content)

        current_date += datetime.timedelta(days=1)

    # Saving all charts from all reports in a combined file
    chartlist_name = f"{active_vendor}_chartlist.txt"
    chartlist_location = os.path.join(output_location, chartlist_name)
    # random shuffling chart list for help in random selecting in excel
    random.shuffle(all_charts)
    with open(chartlist_location, "w") as f:
        for i, chart in enumerate(all_charts):
            if i < len(all_charts) - 1:
                f.write(f"{chart}\n")
            else:
                f.write(f"{chart}")


def generate_all_vendor_reports():
    """
    Generates all reports for all active vendors.

    This function will clear the report base location, generate the member list
    file, and then generate reports for each active vendor using the
    generate_files function.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    clear_folder(report_base)
    generate_member_list(mem_id_start, mem_id_end)
    for vendor in active_vendor_list:
        generate_files(active_vendor=vendor)

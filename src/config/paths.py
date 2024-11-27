import os
from pathlib import Path
from .config import excel_filename

# Project Base Location - Getting the project root directory
current_file = Path(__file__).resolve()
project_location = current_file.parents[2]

# Automation Location
automation_base_loc = os.path.join(project_location, "automation")

# recon_report_load aka rrl
rrl_loc = os.path.join(automation_base_loc, "recon_report_load")
rrl_staging = os.path.join(rrl_loc, "staging")
rrl_input = os.path.join(rrl_loc, "input")
rrl_input_archive = os.path.join(rrl_loc, "input_archive")
rrl_log = os.path.join(rrl_loc, "log")

# recon_report_update aka rru
rru_loc = os.path.join(automation_base_loc, "recon_report_update")
rru_staging = os.path.join(rru_loc, "staging")
rru_input = os.path.join(rru_loc, "input")
rru_input_archive = os.path.join(rru_loc, "input_archive")
rru_log = os.path.join(rru_loc, "log")

# Data Location
data_base_location = os.path.join(project_location, "data")

# Reports Location
report_base = os.path.join(data_base_location, "reports")

# Charts Location
charts_base = os.path.join(data_base_location, "charts")
resource_loc = os.path.join(charts_base, "resources")
charts_drop_off_location = os.path.join(charts_base, "charts_drop_off")
payment_reconciliation_location = os.path.join(charts_base, "payment_reconciliation")

# Excel Setup
excel_setup_location = os.path.join(project_location, "excel_setup")
excel_filepath = os.path.join(excel_setup_location, excel_filename)

import datetime

# Slack Connection Variables
recon_report_load_webhook = (
    ""
)
recon_report_update_webhook = (
    ""
)
bot_auth_token = (
    ""
)
user_auth_token = (
    ""
)
recon_report_load_channel_id = ""
recon_report_update_channel_id = ""

# SQL connection details
server_name = ""
database_name = ""

# File Variables
excel_filename = "financial_reconciliation_generator.xlsm"
recon_load_trigger = r"^[A-Za-z]+_daily_report_\d{8}\.txt$"
# Example: Raven_daily_report_20240327.txt
recon_update_trigger = r"recon_report_update.trigger"

# Date and Time Formats
datetime_format = "%Y%m%dT%H%M%SZ"
date_format = "%Y%m%d"
time_format = "T%H%M%SZ"
time_start = "T063000Z"
time_stop = "T062959Z"
date_range_start = datetime.date(2024, 1, 1)
date_range_end = datetime.date(2024, 6, 30)

# Process Variables
vendor_flag = {"Gryff": 1, "Slyth": 0, "Huffle": 1, "Raven": 1}
active_vendor_list = [key for key, value in vendor_flag.items() if value == 1]

health_systems_list = {
    "Gryff": [
        "LocketHealthNetwork",
        "DiaryMedicalGroup",
        "DiademWellnessSystems",
        "StagShieldHealth",
    ],
    "Huffle": ["CupHealthServices", "RingHealthAlliance", "SnakeWellnessClinic"],
    "Raven": ["CloakHealthSolutions", "ElderHealthCare", "StoneWellnessCentre"],
}


# Report Size Variables
min_chart = 5
max_chart = 1000
mem_id_start = 100
mem_id_end = 1100

from .config import server_name, database_name

# SQL connection string
conn_str = (
    "DRIVER={SQL Server};"
    f"SERVER={server_name};"
    f"DATABASE={database_name};"
    "Trusted_Connection=yes;"
)

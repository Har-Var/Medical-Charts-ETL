import pyodbc
from config import conn_str


def fetch_query(cursor, schema, table_name):
    """
    Fetches a list of chart names from the specified table.

    Parameters
    ----------
    cursor : pyodbc.Cursor
        A cursor object connected to a SQL Server database.
    schema : str
        The name of the schema containing the table.
    table_name : str
        The name of the table to fetch from.

    Returns
    -------
    list
        A list of chart names.
    """
    select_query = f"SELECT chartname FROM {schema}.{table_name}"
    cursor.execute(select_query)
    # Fetch all rows and return a list of chart names
    return [row[0] for row in cursor.fetchall()]


def execute_stored_procedure(procedure_name, *params):
    """
    Executes a stored procedure with the given parameters.

    Parameters
    ----------
    procedure_name : str
        The name of the stored procedure to execute.
    *params : list
        A variable number of parameters to pass to the stored procedure.

    Returns
    -------
    None
    """

    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # Construct the EXEC query
    exec_query = f"EXEC {procedure_name}"

    # If there are parameters, append them to the query
    if params:
        # Join parameters as comma-separated values
        param_list = ", ".join(
            [f"'{param}'" if isinstance(param, str) else str(param) for param in params]
        )
        exec_query += f" {param_list}"

    # Execute the stored procedure
    cursor.execute(exec_query)
    conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()

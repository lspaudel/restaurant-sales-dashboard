import pyodbc
import os
from dotenv import load_dotenv

# Load environment variables from sql_env file
load_dotenv(dotenv_path='sql_env')

db_config = {
    "server": os.getenv("DB_SERVER"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}

# Ensure all environment variables are loaded
if not all(db_config.values()):
    raise ValueError("One or more database configuration values are missing.")

def get_db_connection():
    """Establish and return a database connection."""
    connection_string = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={db_config['server']};"
        f"DATABASE={db_config['database']};"
        f"UID={db_config['user']};"
        f"PWD={db_config['password']};"
        "Trusted_Connection=no;"
    )
    try:
        conn = pyodbc.connect(connection_string)
        print("Connection successful!")
        return conn
    except Exception as e:
        print("Error while connecting:", e)
        raise

if __name__ == '__main__':
    get_db_connection()

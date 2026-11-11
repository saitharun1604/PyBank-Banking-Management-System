
import mysql.connector
from mysql.connector import Error

# MySQL connection settings

DB_CONFIG = {
    "host": "localhost",
    "user": "pybank_user",
    "password": "PyBank@12345",
    "database": "banking_db",
    "port": 3306
}


# Banking business rules
MIN_DEPOSIT = 500
MAX_DEPOSIT = 100000

MIN_WITHDRAWAL = 100
MINIMUM_BALANCE = 1000
DAILY_WITHDRAWAL_LIMIT = 50000

PIN_LENGTH = 4
MAX_FAILED_ATTEMPTS = 3
MIN_OPENING_DEPOSIT = 1000


def get_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)

        if connection.is_connected():
            return connection

    except Error as e:
        print(f"Database connection error: {e}")
        raise

    return None

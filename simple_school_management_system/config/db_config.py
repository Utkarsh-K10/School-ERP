# config/db_config.py
import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",             # Change as per your MySQL setup
            password="yourpassword", # Change as per your MySQL setup
            database="school_db"     # Make sure this database exists
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

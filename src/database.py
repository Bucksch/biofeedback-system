import psycopg2
from psycopg2 import sql

def get_database_connection():
    try:
        connection = psycopg2.connect(
            host="localhost",
            port="5432",
            database="postgres", # Change this to your database name
            user="postgres", # Change this to your username
            password="postgres", # Change this to your password
            sslmode="require"
        )
        return connection
    except psycopg2.Error as error:
        # Handle exception (log error)
        print("Error connecting to the database:", error)

def insert_signal_data(connection, data_time, value):
    try:
        with connection.cursor() as cursor:
            insert_query = sql.SQL("""
                INSERT INTO signal_data (data_time, value)
                VALUES (%s, %s)
            """)
            cursor.execute(insert_query, (data_time, value))
        connection.commit()
    except psycopg2.Error as error:
        connection.rollback()
        # Handle exception (log error)
        print("Error inserting signal data:", error)
        
def insert_extracted_feature(connection, feature, value):
    try:
        with connection.cursor() as cursor:
            insert_query = sql.SQL("""
                INSERT INTO eda_parameters (feature, value, created_at)
                VALUES (%s, %s, NOW())
            """)
            cursor.execute(insert_query, (feature, value))
        connection.commit()
    except psycopg2.Error as error:
        connection.rollback()
        # Handle exception (log error)
        print("Error inserting extracted feature:", error)
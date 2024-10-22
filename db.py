import mysql.connector

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',  # Update with your DB host
            user='poojith',
            password='poojith',
            database='UPS_DB'
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
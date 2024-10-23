import mysql.connector
from mysql.connector import Error

# Function to create a connection to the database
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',          # Update with your DB host
            user='root',      # Update with your DB user
            password='admin',  # Update with your DB password
            database='ups_db'          # Make sure the database name matches
        )
        if connection.is_connected():
            print("✅ Connected to the UPS_DB database.")
        return connection
    except Error as e:
        print(f"❌ Error while connecting to MySQL: {e}")
        return None

# Function to execute a query with parameters (SELECT and non-SELECT queries)
def execute_query(connection, query, params=(), select=False):
    try:
        cursor = connection.cursor()
        cursor.execute(query, params)
        if select:
            # For SELECT queries, fetch and return results
            result = cursor.fetchall()
            cursor.close()
            return result
        else:
            # For INSERT, UPDATE, DELETE, COMMIT the transaction
            connection.commit()
            cursor.close()
    except Error as e:
        print(f"❌ Error executing query: {e}")
    finally:
        cursor.close()

# Function to check if a specific record exists
def check_record_existance(table_name, column_name, value, connection):
    try:
        query = f"SELECT COUNT(*) FROM {table_name} WHERE {column_name} = %s"
        cursor = connection.cursor()
        cursor.execute(query, (value,))
        result = cursor.fetchone()[0]
        cursor.close()
        return result > 0
    except Error as e:
        print(f"❌ Error checking record existence: {e}")
        return False
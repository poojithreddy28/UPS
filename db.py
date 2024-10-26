import mysql.connector
from mysql.connector import Error

# Function to create a connection to the database
def create_connection():
    """
    Establishes a connection to the MySQL database.
    Returns the connection object if successful, otherwise returns None.
    """
    try:
        # Configure database connection details
        connection = mysql.connector.connect(
            host='localhost',          # Database host (typically 'localhost')
            user='poojith',            # Database username
            password='poojith',        # Database password
            database='UPS_DB'          # Target database name
        )
        if connection.is_connected():
            print("✅ Connected to the UPS_DB database.")
        return connection
    except Error as e:
        print(f"❌ Error while connecting to MySQL: {e}")
        return None

# Function to execute a query with parameters (for SELECT and non-SELECT queries)
def execute_query(connection, query, params=(), select=False):
    """
    Executes a given SQL query.
    
    Parameters:
        connection - the MySQL connection object
        query - SQL query to execute
        params - parameters for query placeholders
        select - boolean, set to True for SELECT queries to fetch results
    
    Returns:
        For SELECT queries: returns fetched results
        For non-SELECT queries: commits transaction (INSERT, UPDATE, DELETE)
    """
    try:
        cursor = connection.cursor()
        cursor.execute(query, params)
        if select:
            # Fetch and return results if the query is a SELECT statement
            result = cursor.fetchall()
            cursor.close()
            return result
        else:
            # For INSERT, UPDATE, DELETE, commits transaction
            connection.commit()
            cursor.close()
    except Error as e:
        print(f"❌ Error executing query: {e}")
    finally:
        cursor.close()

# Function to check if a specific record exists
def check_record_existance(table_name, column_name, value, connection):
    """
    Checks for the existence of a specific record in a table.
    
    Parameters:
        table_name - the name of the table to search
        column_name - the column to match the value against
        value - the value to search for
        connection - the MySQL connection object

    Returns:
        True if the record exists, otherwise False.
    """
    try:
        # Build and execute a SELECT COUNT query to check record existence
        query = f"SELECT COUNT(*) FROM {table_name} WHERE {column_name} = %s"
        cursor = connection.cursor()
        cursor.execute(query, (value,))
        result = cursor.fetchone()[0]
        cursor.close()
        return result > 0  # Returns True if count is greater than 0
    except Error as e:
        print(f"❌ Error checking record existence: {e}")
        return False
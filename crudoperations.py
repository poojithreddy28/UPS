from db import create_connection

# CRUD Functions for Users
def create_user(first_name, last_name, email, phone_number, role_id, password):
    conn = create_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO Users (first_name, last_name, email, phone_number, role_id, Password) 
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (first_name, last_name, email, phone_number, role_id, password))
    conn.commit()
    cursor.close()
    conn.close()

def get_all_users():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users")
    results = cursor.fetchall()
    for row in results:
        print(row)
    cursor.close()
    conn.close()

# Similarly, add CRUD functions for Customers, Shipments, Packages, etc.
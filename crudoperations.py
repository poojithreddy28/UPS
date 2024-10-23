from menus import crud_operation_menu, table_list, display_message
from db import create_connection, execute_query, check_record_existance
import datetime

def manage_users(conn):
    while True:
        display_message("USER MANAGEMENT MENU")
        choice = crud_operation_menu("Users")
        
        if choice == "1":
            # Add New User
            first_name = input("Enter First Name: ").strip()
            last_name = input("Enter Last Name: ").strip()
            email = input("Enter Email: ").strip()
            phone_number = input("Enter Phone Number: ").strip()
            role_id = input("Enter Role ID: ").strip()
            password = input("Enter Password: ").strip()
            
            query = "INSERT INTO Users (first_name, last_name, email, phone_number, role_id, password) VALUES (%s, %s, %s, %s, %s, %s)"
            execute_query(conn, query, (first_name, last_name, email, phone_number, role_id, password))
            print("✅ User added successfully.")
            
        elif choice == "2":
             # Read User Data
            user_id = input("Enter User ID to search: ").strip()
            query = "SELECT * FROM Users WHERE user_id = %s"
            results = execute_query(conn, query, (user_id,), select=True)
            
            if results:
                for row in results:
                    print(f"User ID: {row[0]}, Name: {row[1]} {row[2]}, Email: {row[3]}, Phone: {row[4]}, Role ID: {row[5]}")
            else:
                print("⚠️ No matching record found.")

        elif choice == "3":
            # Update User
            user_id = input("Enter User ID to update: ").strip()
            if not check_record_existance("Users", "user_id", user_id, conn):
                print("⚠️ No matching record found.")
                continue
            
            new_first_name = input("Enter New First Name: ").strip()
            new_last_name = input("Enter New Last Name: ").strip()
            new_phone_number = input("Enter New Phone Number: ").strip()
            query = "UPDATE Users SET first_name = %s, last_name = %s, phone_number = %s WHERE user_id = %s"
            execute_query(conn, query, (new_first_name, new_last_name, new_phone_number, user_id))
            print("✅ User updated successfully.")

        elif choice == "4":
            # Delete User
            user_id = input("Enter User ID to delete: ").strip()
            if check_record_existance("Users", "user_id", user_id, conn):
                query = "DELETE FROM Users WHERE user_id = %s"
                execute_query(conn, query, (user_id,))
                print("✅ User deleted successfully.")
            else:
                print("⚠️ No matching record found.")

        elif choice == "5":
            return table_list()
        else:
            print("⚠️ Invalid choice. Please try again.")

def manage_customers(conn):
    while True:
        display_message("CUSTOMER MANAGEMENT MENU")
        choice = crud_operation_menu("Customers")
        
        if choice == "1":
            # Add New Customer
            first_name = input("Enter First Name: ").strip()
            last_name = input("Enter Last Name: ").strip()
            email = input("Enter Email: ").strip()
            phone_number = input("Enter Phone Number: ").strip()
            dob = input("Enter Date of Birth (YYYY-MM-DD): ").strip()
            
            query = """
                INSERT INTO Customers (first_name, last_name, email, phone_number, DOB) 
                VALUES (%s, %s, %s, %s, %s)
            """
            execute_query(conn, query, (first_name, last_name, email, phone_number, dob))
            print("✅ Customer added successfully.")
            
        elif choice == "2":
            # Read Customer Data
            customer_id = input("Enter Customer ID to search: ").strip()
            query = "SELECT * FROM Customers WHERE customer_id = %s"
            results = execute_query(conn, query, (customer_id,), select=True)
            
            if results:
                for row in results:
                    print(f"Customer ID: {row[0]}, Name: {row[1]} {row[2]}, Email: {row[3]}, Phone: {row[4]}, DOB: {row[5]}")
            else:
                print("⚠️ No matching record found.")
                
        elif choice == "3":
            # Update Customer
            customer_id = input("Enter Customer ID to update: ").strip()
            if not check_record_existance("Customers", "customer_id", customer_id, conn):
                print("⚠️ No matching record found.")
                continue
            
            new_first_name = input("Enter New First Name: ").strip()
            new_last_name = input("Enter New Last Name: ").strip()
            new_phone_number = input("Enter New Phone Number: ").strip()
            new_email = input("Enter New Email: ").strip()
            new_dob = input("Enter New Date of Birth (YYYY-MM-DD): ").strip()
            
            query = """
                UPDATE Customers 
                SET first_name = %s, last_name = %s, phone_number = %s, email = %s, DOB = %s 
                WHERE customer_id = %s
            """
            execute_query(conn, query, (new_first_name, new_last_name, new_phone_number, new_email, new_dob, customer_id))
            print("✅ Customer updated successfully.")

        elif choice == "4":
            # Delete Customer
            customer_id = input("Enter Customer ID to delete: ").strip()
            if check_record_existance("Customers", "customer_id", customer_id, conn):
                query = "DELETE FROM Customers WHERE customer_id = %s"
                execute_query(conn, query, (customer_id,))
                print("✅ Customer deleted successfully.")
            else:
                print("⚠️ No matching record found.")

        elif choice == "5":
            return table_list()
        else:
            print("⚠️ Invalid choice. Please try again.")
            
def manage_shipments(conn):
    # CRUD functions for Shipments
    pass

def manage_packages(conn):
    # CRUD functions for Packages
    pass

def manage_payments(conn):
    # CRUD functions for Payments
    pass

# Repeat similarly for other functions...
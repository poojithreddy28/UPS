from menus import crud_operation_menu, table_list, display_message
from db import execute_query, check_record_existance
import re


def validate_email(email):
    """Validate email format"""
    pattern = r"[^@]+@[^@]+\.[^@]+"
    return re.match(pattern, email)

def validate_phone(phone_number):
    """Validate phone number (example: should be 10 digits)"""
    return phone_number.isdigit() and len(phone_number) == 10

def format_record(header, data):
    """Display records interactively"""
    print("\n" + "=" * 50)
    print(f"{header}".center(50))
    print("-" * 50)
    for key, value in data.items():
        print(f"{key:<20}: {value}")
    print("=" * 50)

def manage_users(conn):
    while True:
        display_message("USER MANAGEMENT MENU")
        choice = crud_operation_menu("Users")
        
        if choice == "1":
            # Add New User
            first_name = input("Enter First Name: ").strip()
            last_name = input("Enter Last Name: ").strip()
            email = input("Enter Email: ").strip()
            while not validate_email(email):
                print("⚠️ Invalid email format. Please try again.")
                email = input("Enter Email: ").strip()
                
            phone_number = input("Enter Phone Number: ").strip()
            while not validate_phone(phone_number):
                print("⚠️ Invalid phone number. Please enter a 10-digit number.")
                phone_number = input("Enter Phone Number: ").strip()
                
            role_id = input("Enter Role ID: ").strip()
            password = input("Enter Password: ").strip()
            
            query = "INSERT INTO Users (first_name, last_name, email, phone_number, role_id, password) VALUES (%s, %s, %s, %s, %s, %s)"
            
            try:
                execute_query(conn, query, (first_name, last_name, email, phone_number, role_id, password))
                print("\n" + "=" * 50)
                print("✅ User added successfully.")
            except Exception as e:
                print(f"❌ Error adding user: {e}")
            
        elif choice == "2":
            # Read User Data
            user_id = input("Enter User ID to search: ").strip()
            query = "SELECT * FROM Users WHERE user_id = %s"
            try:
                results = execute_query(conn, query, (user_id,), select=True)
                if results:
                    for row in results:
                        data = {
                            "User ID": row[0],
                            "Name": f"{row[1]} {row[2]}",
                            "Email": row[3],
                            "Phone": row[4],
                            "Role ID": row[5]
                        }
                        format_record("USER RECORD", data)
                else:
                    print("⚠️ No matching record found.")
            except Exception as e:
                print(f"❌ Error reading user data: {e}")

        elif choice == "3":
            # Update User
            user_id = input("Enter User ID to update: ").strip()
            if not check_record_existance("Users", "user_id", user_id, conn):
                print("⚠️ No matching record found.")
                continue
            
            new_first_name = input("Enter New First Name: ").strip()
            new_last_name = input("Enter New Last Name: ").strip()
            new_phone_number = input("Enter New Phone Number: ").strip()
            while not validate_phone(new_phone_number):
                print("⚠️ Invalid phone number. Please enter a 10-digit number.")
                new_phone_number = input("Enter New Phone Number: ").strip()
            
            query = "UPDATE Users SET first_name = %s, last_name = %s, phone_number = %s WHERE user_id = %s"
            try:
                execute_query(conn, query, (new_first_name, new_last_name, new_phone_number, user_id))
                print("✅ User updated successfully.")
            except Exception as e:
                print(f"❌ Error updating user: {e}")

        elif choice == "4":
            # Delete User
            user_id = input("Enter User ID to delete: ").strip()
            if check_record_existance("Users", "user_id", user_id, conn):
                query = "DELETE FROM Users WHERE user_id = %s"
                try:
                    execute_query(conn, query, (user_id,))
                    print("✅ User deleted successfully.")
                except Exception as e:
                    print(f"❌ Error deleting user: {e}")
            else:
                print("⚠️ No matching record found.")

        elif choice == "5":
            return table_list()
        else:
            print("⚠️ Invalid choice. Please try again.")

# 2. Customer Management
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
            print("\n" + "=" * 50)
            print("✅ Customer added successfully.")
            
        elif choice == "2":
            # Read Customer Data
            customer_id = input("Enter Customer ID to search: ").strip()
            query = "SELECT * FROM Customers WHERE customer_id = %s"
            results = execute_query(conn, query, (customer_id,), select=True)
            
            if results:
                for row in results:
                    data = {
                        "Customer ID": row[0],
                        "Name": f"{row[1]} {row[2]}",
                        "Email": row[3],
                        "Phone": row[4],
                        "DOB": row[5]
                    }
                    format_record("CUSTOMER RECORD", data)
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
# 1. Addresses Management
def manage_addresses(conn):
    while True:
        display_message("ADDRESS MANAGEMENT MENU")
        choice = crud_operation_menu("Addresses")
        
        if choice == "1":
            # Add New Address
            try:
                customer_id = input("Enter Customer ID: ").strip()
                street_address = input("Enter Street Address: ").strip()
                city = input("Enter City: ").strip()
                state = input("Enter State: ").strip()
                postal_code = input("Enter Postal Code: ").strip()
                country = input("Enter Country: ").strip()
                
                query = """
                    INSERT INTO Addresses (customer_id, Street_Address, City, State, Postal_Code, Country) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                execute_query(conn, query, (customer_id, street_address, city, state, postal_code, country))
                print("\n" + "=" * 50)
                print("✅ Address added successfully.".center(50))
                print("=" * 50)

            except Exception as e:
                print("\n" + "=" * 50)
                print(f"❌ Error adding address: {str(e)}".center(50))
                print("=" * 50)
            
        elif choice == "2":
            # Read Address Data
            try:
                address_id = input("Enter Address ID to search: ").strip()
                query = "SELECT * FROM Addresses WHERE customer_id = %s"
                results = execute_query(conn, query, (address_id,), select=True)
                
                if results:
                    print("\n" + "=" * 50)
                    print("📍 ADDRESS DETAILS".center(50))
                    print("-" * 50)
                    for row in results:
                        print(f"Customer ID: {row[0]}")
                        print(f"Street Address: {row[1]}")
                        print(f"City: {row[2]}")
                        print(f"State: {row[3]}")
                        print(f"Postal Code: {row[4]}")
                        print(f"Country: {row[5]}")
                        print("-" * 50)
                else:
                    print("\n" + "=" * 50)
                    print("⚠️ No matching record found.".center(50))
                    print("=" * 50)

            except Exception as e:
                print("\n" + "=" * 50)
                print(f"❌ Error reading address data: {str(e)}".center(50))
                print("=" * 50)
                
        elif choice == "3":
            # Update Address
            try:
                address_id = input("Enter Customer ID of Address to update: ").strip()
                if not check_record_existance("Addresses", "customer_id", address_id, conn):
                    print("\n" + "=" * 50)
                    print("⚠️ No matching record found.".center(50))
                    print("=" * 50)
                    continue
                
                new_street_address = input("Enter New Street Address: ").strip()
                new_city = input("Enter New City: ").strip()
                new_state = input("Enter New State: ").strip()
                new_postal_code = input("Enter New Postal Code: ").strip()
                new_country = input("Enter New Country: ").strip()
                
                query = """
                    UPDATE Addresses 
                    SET Street_Address = %s, City = %s, State = %s, Postal_Code = %s, Country = %s
                    WHERE customer_id = %s
                """
                execute_query(conn, query, (new_street_address, new_city, new_state, new_postal_code, new_country, address_id))
                print("\n" + "=" * 50)
                print("✅ Address updated successfully.".center(50))
                print("=" * 50)

            except Exception as e:
                print("\n" + "=" * 50)
                print(f"❌ Error updating address: {str(e)}".center(50))
                print("=" * 50)

        elif choice == "4":
            # Delete Address
            try:
                address_id = input("Enter Customer ID of Address to delete: ").strip()
                if check_record_existance("Addresses", "customer_id", address_id, conn):
                    query = "DELETE FROM Addresses WHERE customer_id = %s"
                    execute_query(conn, query, (address_id,))
                    print("\n" + "=" * 50)
                    print("✅ Address deleted successfully.".center(50))
                    print("=" * 50)
                else:
                    print("\n" + "=" * 50)
                    print("⚠️ No matching record found.".center(50))
                    print("=" * 50)

            except Exception as e:
                print("\n" + "=" * 50)
                print(f"❌ Error deleting address: {str(e)}".center(50))
                print("=" * 50)

        elif choice == "5":
            return table_list()
        else:
            print("\n" + "=" * 50)
            print("⚠️ Invalid choice. Please try again.".center(50))
            print("=" * 50)

def manage_delivery_attempts(conn):
    while True:
        display_message("DELIVERY ATTEMPTS MANAGEMENT MENU")
        choice = crud_operation_menu("Delivery Attempts")
        
        if choice == "1":
            # Add New Delivery Attempt
            try:
                shipment_id = input("Enter Shipment ID: ").strip()
                attempt_date = input("Enter Attempt Date (YYYY-MM-DD): ").strip()
                attempt_status = input("Enter Attempt Status: ").strip()
                
                query = """
                    INSERT INTO DeliveryAttempts (shipment_id, attempt_date, attempt_status) 
                    VALUES (%s, %s, %s)
                """
                execute_query(conn, query, (shipment_id, attempt_date, attempt_status))
                print("\n" + "=" * 50)
                print("✅ Delivery attempt added successfully.".center(50))
                print("=" * 50)
            
            except Exception as e:
                print("\n" + "=" * 50)
                print(f"❌ Error adding delivery attempt: {str(e)}".center(50))
                print("=" * 50)
            
        elif choice == "2":
            # Read Delivery Attempt Data
            try:
                attempt_id = input("Enter Attempt ID to search: ").strip()
                query = "SELECT * FROM DeliveryAttempts WHERE attempt_id = %s"
                results = execute_query(conn, query, (attempt_id,), select=True)
                
                if results:
                    print("\n" + "=" * 50)
                    print("📦 DELIVERY ATTEMPT DETAILS".center(50))
                    print("-" * 50)
                    for row in results:
                        print(f"Attempt ID: {row[0]}")
                        print(f"Shipment ID: {row[1]}")
                        print(f"Attempt Date: {row[2]}")
                        print(f"Attempt Status: {row[3]}")
                        print("-" * 50)
                else:
                    print("\n" + "=" * 50)
                    print("⚠️ No matching record found.".center(50))
                    print("=" * 50)

            except Exception as e:
                print("\n" + "=" * 50)
                print(f"❌ Error reading delivery attempt data: {str(e)}".center(50))
                print("=" * 50)
                
        elif choice == "3":
            # Update Delivery Attempt
            try:
                attempt_id = input("Enter Attempt ID to update: ").strip()
                if not check_record_existance("DeliveryAttempts", "attempt_id", attempt_id, conn):
                    print("\n" + "=" * 50)
                    print("⚠️ No matching record found.".center(50))
                    print("=" * 50)
                    continue
                
                new_attempt_date = input("Enter New Attempt Date (YYYY-MM-DD): ").strip()
                new_attempt_status = input("Enter New Attempt Status: ").strip()
                
                query = """
                    UPDATE DeliveryAttempts 
                    SET attempt_date = %s, attempt_status = %s
                    WHERE attempt_id = %s
                """
                execute_query(conn, query, (new_attempt_date, new_attempt_status, attempt_id))
                print("\n" + "=" * 50)
                print("✅ Delivery attempt updated successfully.".center(50))
                print("=" * 50)

            except Exception as e:
                print("\n" + "=" * 50)
                print(f"❌ Error updating delivery attempt: {str(e)}".center(50))
                print("=" * 50)

        elif choice == "4":
            # Delete Delivery Attempt
            try:
                attempt_id = input("Enter Attempt ID to delete: ").strip()
                if check_record_existance("DeliveryAttempts", "attempt_id", attempt_id, conn):
                    query = "DELETE FROM DeliveryAttempts WHERE attempt_id = %s"
                    execute_query(conn, query, (attempt_id,))
                    print("\n" + "-" * 50)
                    print("✅ Delivery attempt deleted successfully.".center(50))
                    print("-" * 50)
                else:
                    print("\n" + "=" * 50)
                    print("⚠️ No matching record found.".center(50))
                    print("=" * 50)

            except Exception as e:
                print("\n" + "=" * 50)
                print(f"❌ Error deleting delivery attempt: {str(e)}".center(50))
                print("=" * 50)

        elif choice == "5":
            return table_list()
        else:
            print("\n" + "=" * 50)
            print("⚠️ Invalid choice. Please try again.".center(50))
            print("=" * 50)

def manage_package_dimension(conn):
    while True:
        display_message("PACKAGE DIMENSION MANAGEMENT MENU")
        choice = crud_operation_menu("Package Dimensions")
        
        if choice == "1":
            # Add New Package Dimension
            try:
                package_id = input("Enter Package ID: ").strip()
                length = input("Enter Length: ").strip()
                width = input("Enter Width: ").strip()
                height = input("Enter Height: ").strip()
                
                query = """
                    INSERT INTO PackageDimension (package_id, length, width, height) 
                    VALUES (%s, %s, %s, %s)
                """
                execute_query(conn, query, (package_id, length, width, height))
                print("\n" + "=" * 50)
                print("✅ Package dimension added successfully.".center(50))
                print("=" * 50)
            
            except Exception as e:
                print("\n" + "=" * 50)
                print(f"❌ Error adding package dimension: {str(e)}".center(50))
                print("=" * 50)
                
        elif choice == "2":
            # Read Package Dimension Data
            try:
                package_id = input("Enter Package ID to search: ").strip()
                query = "SELECT * FROM PackageDimension WHERE package_id = %s"
                results = execute_query(conn, query, (package_id,), select=True)
                
                if results:
                    print("\n" + "=" * 50)
                    print("📏 PACKAGE DIMENSION DETAILS".center(50))
                    print("-" * 50)
                    for row in results:
                        print(f"Package ID: {row[0]}")
                        print(f"Length: {row[1]}")
                        print(f"Width: {row[2]}")
                        print(f"Height: {row[3]}")
                        print("-" * 50)
                else:
                    print("\n" + "=" * 50)
                    print("⚠️ No matching record found.".center(50))
                    print("=" * 50)
                    
            except Exception as e:
                print("\n" + "=" * 50)
                print(f"❌ Error reading package dimension data: {str(e)}".center(50))
                print("=" * 50)
                
        elif choice == "3":
            # Update Package Dimension
            try:
                package_id = input("Enter Package ID to update: ").strip()
                if not check_record_existance("PackageDimension", "package_id", package_id, conn):
                    print("\n" + "=" * 50)
                    print("⚠️ No matching record found.".center(50))
                    print("=" * 50)
                    continue
                
                new_length = input("Enter New Length: ").strip()
                new_width = input("Enter New Width: ").strip()
                new_height = input("Enter New Height: ").strip()
                
                query = """
                    UPDATE PackageDimension 
                    SET length = %s, width = %s, height = %s
                    WHERE package_id = %s
                """
                execute_query(conn, query, (new_length, new_width, new_height, package_id))
                print("\n" + "=" * 50)
                print("✅ Package dimension updated successfully.".center(50))
                print("=" * 50)

            except Exception as e:
                print("\n" + "=" * 50)
                print(f"❌ Error updating package dimension: {str(e)}".center(50))
                print("=" * 50)

        elif choice == "4":
            # Delete Package Dimension
            try:
                package_id = input("Enter Package ID to delete dimensions: ").strip()
                if check_record_existance("PackageDimension", "package_id", package_id, conn):
                    query = "DELETE FROM PackageDimension WHERE package_id = %s"
                    execute_query(conn, query, (package_id,))
                    print("\n" + "=" * 50)
                    print("✅ Package dimension deleted successfully.".center(50))
                    print("=" * 50)
                else:
                    print("\n" + "=" * 50)
                    print("⚠️ No matching record found.".center(50))
                    print("=" * 50)
                    
            except Exception as e:
                print("\n" + "=" * 50)
                print(f"❌ Error deleting package dimension: {str(e)}".center(50))
                print("=" * 50)

        elif choice == "5":
            return table_list()
        else:
            print("\n" + "=" * 50)
            print("⚠️ Invalid choice. Please try again.".center(50))
            print("=" * 50)


def manage_package_status(conn):

    pass

def manage_pickup_requests(conn):

    pass

def manage_user_role(conn):
    
    pass



from menus import crud_operation_menu, table_list, display_message
from db import execute_query, check_record_existance
import re
import datetime


#Handles CRUD operations for various entities
def manage_basic_crud_operations(conn):
    """
    Handles basic CRUD operations for various entities like Users, Customers, etc.
    """
    while True:
        print("\n" + "=" * 50)
        print(f"\033[1m🗂️ BASIC CRUD OPERATIONS MENU 🗂️\033[0m".center(50))
        print("Choose an entity to manage.".center(50))
        print("=" * 50)
        print("1. 🧑 Manage Users")
        print("2. 👥 Manage Customers")
        print("3. 🚚 Manage Shipments")
        print("4. 📦 Manage Packages")
        print("5. 💳 Manage Payments")
        print("6. 🏠 Manage Addresses")
        print("7. 🕵️‍♂️ Manage Delivery Attempts")
        print("8. 📏 Manage Package Dimensions")
        print("9. 📄 Manage Package Status")
        print("10. 📋 Manage Pickup Requests")
        print("11. 🔒 Manage User Roles")
        print("12. 🔙 Return to Main Menu")
        print("=" * 50)

        choice = input("👉 Select an entity to manage (1-12): ").strip()

        if choice == "1":
            manage_users(conn)  # Manage user records
        elif choice == "2":
            manage_customers(conn)  # Manage customer records
        elif choice == "3":
            manage_shipments(conn)  # Manage shipment records
        elif choice == "4":
            manage_packages(conn)  # Manage package records
        elif choice == "5":
            manage_payments(conn)  # Manage payment records
        elif choice == "6":
            manage_addresses(conn)  # Manage address records
        elif choice == "7":
            manage_delivery_attempts(conn)  # Manage delivery attempt records
        elif choice == "8":
            manage_package_dimension(conn)  # Manage package dimensions records
        elif choice == "9":
            manage_package_status(conn)  # Manage package status records
        elif choice == "10":
            manage_pickup_requests(conn)  # Manage pickup request records
        elif choice == "11":
            manage_user_role(conn)  # Manage user role records
        elif choice == "12":
            print("🔙 Returning to Main Menu")
            break
        else:
            print("⚠️ Invalid option, please choose again.")

# Helper functions
def validate_email(email):
    """Validate email format using regex"""
    pattern = r"[^@]+@[^@]+\.[^@]+"
    return re.match(pattern, email)

def validate_phone(phone_number):
    """Validate if phone number is 10 digits long"""
    return phone_number.isdigit() and len(phone_number) == 10

def format_record(header, data):
    """Format and display records with a header and key-value pairs"""
    print("\n" + "=" * 50)
    print(f"{header}".center(50))
    print("-" * 50)
    for key, value in data.items():
        print(f"{key:<20}: {value}")
    print("=" * 50)

# Manage Users
def manage_users(conn):
    """Handle CRUD operations for Users"""
    while True:
        display_message("USER MANAGEMENT MENU")
        choice = crud_operation_menu("Users")
        
        if choice == "1":
            # Add New User
            try:
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
                execute_query(conn, query, (first_name, last_name, email, phone_number, role_id, password))
                print("\n" + "=" * 50)
                print("✅ User added successfully.")
            except Exception as e:
                print(f"❌ Error adding user: {e}")
            
        elif choice == "2":
            # Read User Data
            try:
                user_id = input("Enter User ID to search: ").strip()
                query = "SELECT * FROM Users WHERE user_id = %s"
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
            try:
                user_id = input("Enter User ID to update: ").strip()
                if not check_record_existance("Users", "user_id", user_id, conn):
                    print("⚠️ No matching record found.")
                
                new_first_name = input("Enter New First Name: ").strip()
                new_last_name = input("Enter New Last Name: ").strip()
                new_phone_number = input("Enter New Phone Number: ").strip()
                while not validate_phone(new_phone_number):
                    print("⚠️ Invalid phone number. Please enter a 10-digit number.")
                    new_phone_number = input("Enter New Phone Number: ").strip()
                
                query = "UPDATE Users SET first_name = %s, last_name = %s, phone_number = %s WHERE user_id = %s"
                execute_query(conn, query, (new_first_name, new_last_name, new_phone_number, user_id))
                print("✅ User updated successfully.")
            except Exception as e:
                print(f"❌ Error updating user: {e}")

        elif choice == "4":
            # Delete User
            try:
                user_id = input("Enter User ID to delete: ").strip()
                if check_record_existance("Users", "user_id", user_id, conn):
                    query = "DELETE FROM Users WHERE user_id = %s"
                    execute_query(conn, query, (user_id,))
                    print("✅ User deleted successfully.")
                else:
                    print("⚠️ No matching record found.")
            except Exception as e:
                print(f"❌ Error deleting user: {e}")

        elif choice == "5":
            return table_list()
        else:
            print("⚠️ Invalid choice. Please try again.")

# Manage Customers
def manage_customers(conn):
    """Handle CRUD operations for Customers"""
    while True:
        display_message("CUSTOMER MANAGEMENT MENU")
        choice = crud_operation_menu("Customers")
        
        if choice == "1":
            # Add New Customer
            try:
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
                
                dob = input("Enter Date of Birth (YYYY-MM-DD): ").strip()
                query = """
                    INSERT INTO Customers (first_name, last_name, email, phone_number, DOB) 
                    VALUES (%s, %s, %s, %s, %s)
                """
                execute_query(conn, query, (first_name, last_name, email, phone_number, dob))
                print("\n" + "=" * 50)
                print("✅ Customer added successfully.")
            except Exception as e:
                print(f"❌ Error adding customer: {e}")
            
        elif choice == "2":
            # Read Customer Data
            try:
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
            except Exception as e:
                print(f"❌ Error reading customer data: {e}")
                
        elif choice == "3":
            # Update Customer
            try:
                customer_id = input("Enter Customer ID to update: ").strip()
                if not check_record_existance("Customers", "customer_id", customer_id, conn):
                    print("⚠️ No matching record found.")
                
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
            except Exception as e:
                print(f"❌ Error updating customer: {e}")

        elif choice == "4":
            # Delete Customer
            try:
                customer_id = input("Enter Customer ID to delete: ").strip()
                if check_record_existance("Customers", "customer_id", customer_id, conn):
                    query = "DELETE FROM Customers WHERE customer_id = %s"
                    execute_query(conn, query, (customer_id,))
                    print("✅ Customer deleted successfully.")
                else:
                    print("⚠️ No matching record found.")
            except Exception as e:
                print(f"❌ Error deleting customer: {e}")

        elif choice == "5":
            return table_list()
        else:
            print("⚠️ Invalid choice. Please try again.")

# Manage Shipments
def manage_shipments(conn):
    """Handle CRUD operations for Shipments"""
    while True:
        display_message("SHIPMENT MANAGEMENT MENU")
        choice = crud_operation_menu("Shipments")
        
        if choice == "1":
            # Add New Shipment
            try:
                customer_id = input("Enter Customer ID: ").strip()
                shipment_status = input("Enter Shipment Status: ").strip()
                shipment_type = input("Enter Shipment Type: ").strip()
                shipment_date = input("Enter Shipment Date (YYYY-MM-DD HH:MM:SS): ").strip()
                user_id = input("Enter User ID: ").strip()

                query = """
                    INSERT INTO Shipments (customer_id, shipment_status, shipment_type, shipment_date, user_id) 
                    VALUES (%s, %s, %s, %s, %s)
                """
                execute_query(conn, query, (customer_id, shipment_status, shipment_type, shipment_date, user_id))
                print("✅ Shipment added successfully.")
            except Exception as e:
                print(f"❌ Error adding shipment: {e}")
        
        elif choice == "2":
            # Read Shipment Data
            try:
                shipment_id = input("Enter Shipment ID to search: ").strip()
                query = "SELECT * FROM Shipments WHERE shipment_id = %s"
                results = execute_query(conn, query, (shipment_id,), select=True)
                
                if results:
                    for row in results:
                        data = {
                            "Shipment ID": row[0],
                            "Customer ID": row[1],
                            "Shipment Status": row[2],
                            "Shipment Type": row[3],
                            "Shipment Date": row[4],
                            "User ID": row[5]
                        }
                        format_record("SHIPMENT RECORD", data)
                else:
                    print("⚠️ No matching record found.")
            except Exception as e:
                print(f"❌ Error reading shipment data: {e}")
        
        elif choice == "3":
            # Update Shipment
            try:
                shipment_id = input("Enter Shipment ID to update: ").strip()
                if not check_record_existance("Shipments", "shipment_id", shipment_id, conn):
                    print("⚠️ No matching record found.")
                
                new_status = input("Enter New Shipment Status: ").strip()
                new_type = input("Enter New Shipment Type: ").strip()
                new_date = input("Enter New Shipment Date (YYYY-MM-DD HH:MM:SS): ").strip()
                
                query = """
                    UPDATE Shipments 
                    SET shipment_status = %s, shipment_type = %s, shipment_date = %s
                    WHERE shipment_id = %s
                """
                execute_query(conn, query, (new_status, new_type, new_date, shipment_id))
                print("✅ Shipment updated successfully.")
            except Exception as e:
                print(f"❌ Error updating shipment: {e}")
        
        elif choice == "4":
            # Delete Shipment
            try:
                shipment_id = input("Enter Shipment ID to delete: ").strip()
                if check_record_existance("Shipments", "shipment_id", shipment_id, conn):
                    query = "DELETE FROM Shipments WHERE shipment_id = %s"
                    execute_query(conn, query, (shipment_id,))
                    print("✅ Shipment deleted successfully.")
                else:
                    print("⚠️ No matching record found.")
            except Exception as e:
                print(f"❌ Error deleting shipment: {e}")
        
        elif choice == "5":
            return table_list()
        else:
            print("⚠️ Invalid choice. Please try again.")

# Manage Packages
def manage_packages(conn):
    """Handle CRUD operations for Packages"""
    while True:
        display_message("PACKAGE MANAGEMENT MENU")
        choice = crud_operation_menu("Packages")
        
        if choice == "1":
            # Add New Package
            try:
                shipment_id = input("Enter Shipment ID: ").strip()
                weight = input("Enter Weight: ").strip()
                contents_description = input("Enter Contents Description: ").strip()
                delivery_confirmation = input("Enter Delivery Confirmation (True/False): ").strip()

                query = """
                    INSERT INTO Packages (shipment_id, weight, contents_description, delivery_confirmation) 
                    VALUES (%s, %s, %s, %s)
                """
                execute_query(conn, query, (shipment_id, weight, contents_description, delivery_confirmation))
                print("✅ Package added successfully.")
            except Exception as e:
                print(f"❌ Error adding package: {e}")
        
        elif choice == "2":
            # Read Package Data
            try:
                package_id = input("Enter Package ID to search: ").strip()
                query = "SELECT * FROM Packages WHERE package_id = %s"
                results = execute_query(conn, query, (package_id,), select=True)
                
                if results:
                    for row in results:
                        data = {
                            "Package ID": row[0],
                            "Shipment ID": row[1],
                            "Weight": row[2],
                            "Contents Description": row[3],
                            "Delivery Confirmation": row[4]
                        }
                        format_record("PACKAGE RECORD", data)
                else:
                    print("⚠️ No matching record found.")
            except Exception as e:
                print(f"❌ Error reading package data: {e}")
        
        elif choice == "3":
            # Update Package
            try:
                package_id = input("Enter Package ID to update: ").strip()
                if not check_record_existance("Packages", "package_id", package_id, conn):
                    print("⚠️ No matching record found.")
                
                new_weight = input("Enter New Weight: ").strip()
                new_description = input("Enter New Contents Description: ").strip()
                new_confirmation = input("Enter New Delivery Confirmation (True/False): ").strip()
                
                query = """
                    UPDATE Packages 
                    SET weight = %s, contents_description = %s, delivery_confirmation = %s
                    WHERE package_id = %s
                """
                execute_query(conn, query, (new_weight, new_description, new_confirmation, package_id))
                print("✅ Package updated successfully.")
            except Exception as e:
                print(f"❌ Error updating package: {e}")
        
        elif choice == "4":
            # Delete Package
            try:
                package_id = input("Enter Package ID to delete: ").strip()
                if check_record_existance("Packages", "package_id", package_id, conn):
                    query = "DELETE FROM Packages WHERE package_id = %s"
                    execute_query(conn, query, (package_id,))
                    print("✅ Package deleted successfully.")
                else:
                    print("⚠️ No matching record found.")
            except Exception as e:
                print(f"❌ Error deleting package: {e}")
        
        elif choice == "5":
            return table_list()
        else:
            print("⚠️ Invalid choice. Please try again.")

# Manage Payments
def manage_payments(conn):
    """Handle CRUD operations for Payments"""
    while True:
        display_message("PAYMENT MANAGEMENT MENU")
        choice = crud_operation_menu("Payments")
        
        if choice == "1":
            # Add New Payment
            try:
                customer_id = input("Enter Customer ID: ").strip()
                amount = input("Enter Amount: ").strip()
                payment_date = input("Enter Payment Date (YYYY-MM-DD): ").strip()
                payment_method = input("Enter Payment Method: ").strip()

                query = """
                    INSERT INTO Payments (customer_id, amount, payment_date, payment_method) 
                    VALUES (%s, %s, %s, %s)
                """
                execute_query(conn, query, (customer_id, amount, payment_date, payment_method))
                print("✅ Payment added successfully.")
            except Exception as e:
                print(f"❌ Error adding payment: {e}")
        
        elif choice == "2":
            # Read Payment Data
            try:
                payment_id = input("Enter Payment ID to search: ").strip()
                query = "SELECT * FROM Payments WHERE payment_id = %s"
                results = execute_query(conn, query, (payment_id,), select=True)
                
                if results:
                    for row in results:
                        data = {
                            "Payment ID": row[0],
                            "Customer ID": row[1],
                            "Amount": row[2],
                            "Payment Date": row[3],
                            "Payment Method": row[4]
                        }
                        format_record("PAYMENT RECORD", data)
                else:
                    print("⚠️ No matching record found.")
            except Exception as e:
                print(f"❌ Error reading payment data: {e}")
        
        elif choice == "3":
            # Update Payment
            try:
                payment_id = input("Enter Payment ID to update: ").strip()
                if not check_record_existance("Payments", "payment_id", payment_id, conn):
                    print("⚠️ No matching record found.")
                
                new_amount = input("Enter New Amount: ").strip()
                new_payment_date = input("Enter New Payment Date (YYYY-MM-DD): ").strip()
                new_method = input("Enter New Payment Method: ").strip()
                
                query = """
                    UPDATE Payments 
                    SET amount = %s, payment_date = %s, payment_method = %s
                    WHERE payment_id = %s
                """
                execute_query(conn, query, (new_amount, new_payment_date, new_method, payment_id))
                print("✅ Payment updated successfully.")
            except Exception as e:
                print(f"❌ Error updating payment: {e}")
        
        elif choice == "4":
            # Delete Payment
            try:
                payment_id = input("Enter Payment ID to delete: ").strip()
                if check_record_existance("Payments", "payment_id", payment_id, conn):
                    query = "DELETE FROM Payments WHERE payment_id = %s"
                    execute_query(conn, query, (payment_id,))
                    print("✅ Payment deleted successfully.")
                else:
                    print("⚠️ No matching record found.")
            except Exception as e:
                print(f"❌ Error deleting payment: {e}")
        
        elif choice == "5":
            return table_list()
        else:
            print("⚠️ Invalid choice. Please try again.")

def manage_addresses(conn):
    """Handle CRUD operations for Addresses"""
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
    """Handle CRUD operations for Delivery Attempts"""
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


def manage_package_status(conn):
    valid_status_types = {"Shipped", "Pending", "In Transit", "Delivered", "Cancelled"}

    while True:
        display_message("PACKAGE STATUS MANAGEMENT MENU")
        choice = crud_operation_menu("Package Status")

        if choice == "1":
            # Add New Status
            package_id = input("Enter Package ID: ").strip()
            
            # Check if package_id exists in Packages table
            if not check_record_existance("Packages", "package_id", package_id, conn):
                print("\n" + "=" * 50)
                print("⚠️ Package ID does not exist. Please enter a valid Package ID.".center(50))
                print("=" * 50)
                continue

            status_type = input("Enter Status Type: ").strip()
            
            # Validate status_type
            if status_type not in valid_status_types:
                print("\n" + "=" * 50)
                print("⚠️ Invalid status type. Please enter one of the following: Shipped, Pending, In Transit, Delivered, Cancelled.".center(50))
                print("=" * 50)
                continue

            query = """
            INSERT INTO PackageStatus (package_id, status_type)
            VALUES (%s, %s)
            """
            
            try:
                execute_query(conn, query, (package_id, status_type))
                print("\n" + "=" * 50)
                print("✅ Package status added successfully.".center(50))
                print("=" * 50)
            except Exception as e:
                print("\n" + "=" * 50)
                print(f"❌ Error adding package status: {str(e)}".center(50))
                print("=" * 50)

        elif choice == "2":
            # Read Status History
            try:
                package_id = input("Enter Package ID to view status history: ").strip()
                query = "SELECT * FROM PackageStatus WHERE package_id = %s ORDER BY status_timestamp"
                results = execute_query(conn, query, (package_id,), select=True)
                
                if results:
                    print("\n" + "=" * 50)
                    print("📄 PACKAGE STATUS HISTORY".center(50))
                    print("-" * 50)
                    for row in results:
                        print(f"Status ID: {row[0]}")
                        print(f"Package ID: {row[1]}")
                        print(f"Status Type: {row[2]}")
                        print(f"Timestamp: {row[3]}")
                        print("-" * 50)
                else:
                    print("\n" + "=" * 50)
                    print("⚠️ No matching records found.".center(50))
                    print("=" * 50)
            except Exception as e:
                print("\n" + "=" * 50)
                print(f"❌ Error reading package status history: {str(e)}".center(50))
                print("=" * 50)

        elif choice == "3":
            # Update Status Entry
            try:
                status_id = input("Enter Status ID to update: ").strip()
                
                if not check_record_existance("PackageStatus", "status_id", status_id, conn):
                    print("\n" + "=" * 50)
                    print("⚠️ No matching record found.".center(50))
                    print("=" * 50)
                    continue

                new_status_type = input("Enter New Status Type: ").strip()
                
                # Validate new_status_type
                if new_status_type not in valid_status_types:
                    print("\n" + "=" * 50)
                    print("⚠️ Invalid status type. Please enter one of the following: Shipped, Pending, In Transit, Delivered, Cancelled.".center(50))
                    print("=" * 50)
                    continue

                query = """
                UPDATE PackageStatus
                SET status_type = %s
                WHERE status_id = %s
                """
                
                execute_query(conn, query, (new_status_type, status_id))
                
                print("\n" + "=" * 50)
                print("✅ Package status updated successfully.".center(50))
                print("=" * 50)
            except Exception as e:
                print("\n" + "=" * 50)
                print(f"❌ Error updating package status: {str(e)}".center(50))
                print("=" * 50)

        elif choice == "4":
            # Delete Status Record
            try:
                status_id = input("Enter Status ID to delete: ").strip()
                
                if check_record_existance("PackageStatus", "status_id", status_id, conn):
                    query = "DELETE FROM PackageStatus WHERE status_id = %s"
                    execute_query(conn, query, (status_id,))
                    
                    print("\n" + "=" * 50)
                    print("✅ Package status deleted successfully.".center(50))
                    print("=" * 50)
                else:
                    print("\n" + "=" * 50)
                    print("⚠️ No matching record found.".center(50))
                    print("=" * 50)
            except Exception as e:
                print("\n" + "=" * 50)
                print(f"❌ Error deleting package status: {str(e)}".center(50))
                print("=" * 50)

        elif choice == "5":
            # Return to Main Menu
            return table_list()

        else:
            print("\n" + "=" * 50)
            print("⚠️ Invalid choice. Please try again.".center(50))
            print("=" * 50)


import datetime

def validate_date(date_text):
    """Validate date format (YYYY-MM-DD)."""
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False
# Manage Pickup Requests
def manage_pickup_requests(conn):
    """Handle CRUD operations for Pickup Requests"""
    while True:
        display_message("PICKUP REQUEST MANAGEMENT MENU")
        choice = crud_operation_menu("Pickup Requests")

        if choice == "1":
            # Register Pickup Request
            try:
                customer_id = input("Enter Customer ID: ").strip()
                pickup_date = input("Enter Pickup Date (YYYY-MM-DD): ").strip()
                pickup_status = input("Enter Pickup Status: ").strip()

                # Validate customer ID and date format
                if not check_record_existance("Customers", "customer_id", customer_id, conn):
                    print("⚠️ Customer ID does not exist. Please enter a valid Customer ID.")
                elif not validate_date(pickup_date):
                    print("⚠️ Invalid date format. Please enter the date in YYYY-MM-DD format.")
                else:
                    query = """
                        INSERT INTO Pickup_Requests (customer_id, pickup_date, pickup_status)
                        VALUES (%s, %s, %s)
                    """
                    execute_query(conn, query, (customer_id, pickup_date, pickup_status))
                    print("✅ Pickup request registered successfully.")
            except Exception as e:
                print(f"❌ Error registering pickup request: {e}")

        elif choice == "2":
            # View Pickup Records
            try:
                request_id = input("Enter Pickup Request ID to search: ").strip()
                query = "SELECT * FROM Pickup_Requests WHERE request_id = %s"
                results = execute_query(conn, query, (request_id,), select=True)

                if results:
                    for row in results:
                        data = {
                            "Request ID": row[0],
                            "Customer ID": row[1],
                            "Pickup Date": row[2],
                            "Pickup Status": row[3]
                        }
                        format_record("PICKUP REQUEST DETAILS", data)
                else:
                    print("⚠️ No matching record found.")
            except Exception as e:
                print(f"❌ Error viewing pickup records: {e}")

        elif choice == "3":
            # Edit Pickup Information
            try:
                request_id = input("Enter Pickup Request ID to update: ").strip()
                if not check_record_existance("Pickup_Requests", "request_id", request_id, conn):
                    print("⚠️ No matching record found.")
                
                new_pickup_date = input("Enter New Pickup Date (YYYY-MM-DD): ").strip()
                new_pickup_status = input("Enter New Pickup Status: ").strip()

                if not validate_date(new_pickup_date):
                    print("⚠️ Invalid date format. Please enter the date in YYYY-MM-DD format.")
                else:
                    query = """
                        UPDATE Pickup_Requests
                        SET pickup_date = %s, pickup_status = %s
                        WHERE request_id = %s
                    """
                    execute_query(conn, query, (new_pickup_date, new_pickup_status, request_id))
                    print("✅ Pickup information updated successfully.")
            except Exception as e:
                print(f"❌ Error updating pickup information: {e}")

        elif choice == "4":
            # Delete Pickup Request
            try:
                request_id = input("Enter Pickup Request ID to delete: ").strip()
                if check_record_existance("Pickup_Requests", "request_id", request_id, conn):
                    query = "DELETE FROM Pickup_Requests WHERE request_id = %s"
                    execute_query(conn, query, (request_id,))
                    print("✅ Pickup request deleted successfully.")
                else:
                    print("⚠️ No matching record found.")
            except Exception as e:
                print(f"❌ Error deleting pickup request: {e}")

        elif choice == "5":
            return table_list()
        else:
            print("⚠️ Invalid choice. Please try again.")

# Manage Package Dimensions
def manage_package_dimension(conn):
    """Handle CRUD operations for Package Dimensions"""
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
                print("✅ Package dimension added successfully.")
            except Exception as e:
                print(f"❌ Error adding package dimension: {e}")

        elif choice == "2":
            # Read Package Dimension Data
            try:
                package_id = input("Enter Package ID to search: ").strip()
                query = "SELECT * FROM PackageDimension WHERE package_id = %s"
                results = execute_query(conn, query, (package_id,), select=True)

                if results:
                    for row in results:
                        data = {
                            "Package ID": row[0],
                            "Length": row[1],
                            "Width": row[2],
                            "Height": row[3]
                        }
                        format_record("PACKAGE DIMENSION DETAILS", data)
                else:
                    print("⚠️ No matching record found.")
            except Exception as e:
                print(f"❌ Error reading package dimension data: {e}")

        elif choice == "3":
            # Update Package Dimension
            try:
                package_id = input("Enter Package ID to update: ").strip()
                if not check_record_existance("PackageDimension", "package_id", package_id, conn):
                    print("⚠️ No matching record found.")
                
                new_length = input("Enter New Length: ").strip()
                new_width = input("Enter New Width: ").strip()
                new_height = input("Enter New Height: ").strip()

                query = """
                    UPDATE PackageDimension 
                    SET length = %s, width = %s, height = %s
                    WHERE package_id = %s
                """
                execute_query(conn, query, (new_length, new_width, new_height, package_id))
                print("✅ Package dimension updated successfully.")
            except Exception as e:
                print(f"❌ Error updating package dimension: {e}")

        elif choice == "4":
            # Delete Package Dimension
            try:
                package_id = input("Enter Package ID to delete dimensions: ").strip()
                if check_record_existance("PackageDimension", "package_id", package_id, conn):
                    query = "DELETE FROM PackageDimension WHERE package_id = %s"
                    execute_query(conn, query, (package_id,))
                    print("✅ Package dimension deleted successfully.")
                else:
                    print("⚠️ No matching record found.")
            except Exception as e:
                print(f"❌ Error deleting package dimension: {e}")

        elif choice == "5":
            return table_list()
        else:
            print("⚠️ Invalid choice. Please try again.")

# Manage User Roles
def manage_user_role(conn):
    """Handle CRUD operations for User Roles"""
    while True:
        display_message("USER ROLES MANAGEMENT MENU")
        choice = crud_operation_menu("User Roles")

        if choice == "1":
            # Add New Role
            try:
                role_name = input("Enter Role Name: ").strip()
                query = """
                    INSERT INTO user_role (role_name)
                    VALUES (%s)
                """
                execute_query(conn, query, (role_name,))
                print("✅ Role added successfully.")
            except Exception as e:
                print(f"❌ Error adding role: {e}")

        elif choice == "2":
            # View Role Records
            try:
                role_id = input("Enter Role ID to search: ").strip()
                query = "SELECT * FROM user_role WHERE role_id = %s"
                results = execute_query(conn, query, (role_id,), select=True)

                if results:
                    for row in results:
                        data = {
                            "Role ID": row[0],
                            "Role Name": row[1]
                        }
                        format_record("ROLE DETAILS", data)
                else:
                    print("⚠️ No matching record found.")
            except Exception as e:
                print(f"❌ Error viewing role records: {e}")

        elif choice == "3":
            # Update Role Details
            try:
                role_id = input("Enter Role ID to update: ").strip()
                if not check_record_existance("user_role", "role_id", role_id, conn):
                    print("⚠️ No matching record found.")
                
                new_role_name = input("Enter New Role Name: ").strip()
                query = """
                    UPDATE user_role
                    SET role_name = %s
                    WHERE role_id = %s
                """
                execute_query(conn, query, (new_role_name, role_id))
                print("✅ Role updated successfully.")
            except Exception as e:
                print(f"❌ Error updating role details: {e}")

        elif choice == "4":
            # Delete Role
            try:
                role_id = input("Enter Role ID to delete: ").strip()
                if check_record_existance("user_role", "role_id", role_id, conn):
                    query = "DELETE FROM user_role WHERE role_id = %s"
                    execute_query(conn, query, (role_id,))
                    print("✅ Role deleted successfully.")
                else:
                    print("⚠️ No matching record found.")
            except Exception as e:
                print(f"❌ Error deleting role: {e}")

        elif choice == "5":
            return table_list()
        else:
            print("⚠️ Invalid choice. Please try again.")
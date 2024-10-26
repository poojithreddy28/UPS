from db import create_connection
from crudoperations import (
    manage_users, manage_customers, manage_shipments, manage_packages, manage_payments,
    manage_addresses, manage_delivery_attempts, manage_package_dimension, manage_package_status,
    manage_pickup_requests, manage_user_role,
)
from menus import table_list

def start_application():
    """
    Entry point for the application.
    Establishes database connection and allows users to perform CRUD operations
    on various entities through a menu-driven interface.
    """
    # Establish a connection to the database
    conn = create_connection()
    if not conn:
        # If the connection fails, display an error message and exit the application
        print("❌ Unable to connect to the database. Exiting...")
        return

    # Continuously display the main menu until the user chooses to exit
    while True:
        table_choice = table_list()
        
        # Based on user input, navigate to the corresponding CRUD operation
        if table_choice == "1":
            manage_users(conn)  # Manage user records
        elif table_choice == "2":
            manage_customers(conn)  # Manage customer records
        elif table_choice == "3":
            manage_shipments(conn)  # Manage shipment records
        elif table_choice == "4":
            manage_packages(conn)  # Manage package records
        elif table_choice == "5":
            manage_payments(conn)  # Manage payment records
        elif table_choice == "6":
            manage_addresses(conn)  # Manage address records
        elif table_choice == "7":
            manage_delivery_attempts(conn)  # Manage delivery attempt records
        elif table_choice == "8":
            manage_package_dimension(conn)  # Manage package dimension records
        elif table_choice == "9":
            manage_package_status(conn)  # Manage package status records
        elif table_choice == "10":
            manage_pickup_requests(conn)  # Manage pickup request records
        elif table_choice == "11":
            manage_user_role(conn)  # Manage user role records
        elif table_choice == "12":
            # If user selects "12", exit the application
            print("👋 Exiting... Have a great day!")
            conn.close()  # Close the database connection before exiting
            break
        else:
            # If an invalid option is selected, prompt the user to choose again
            print("⚠️ Invalid option, please choose again.")

if __name__ == "__main__":
    # Start the application when the script is run
    start_application()
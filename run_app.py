from db import create_connection
from crudoperations import manage_users, manage_customers, manage_shipments, manage_packages, manage_payments
from menus import table_list  # Ensure you import table_list

def start_application():
    conn = create_connection()
    if not conn:
        print("❌ Unable to connect to the database. Exiting...")
        return

    while True:
        table_choice = table_list()
        
        if table_choice == "1":
            manage_users(conn)
        elif table_choice == "2":
            manage_customers(conn)
        elif table_choice == "3":
            manage_shipments(conn)
        elif table_choice == "4":
            manage_packages(conn)
        elif table_choice == "5":
            manage_payments(conn)
        elif table_choice == "6":
            print("👋 Exiting... Have a great day!")
            conn.close()  # Close the database connection before exiting
            break
        else:
            print("⚠️ Invalid option, please choose again.")

if __name__ == "__main__":
    start_application()
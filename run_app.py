from complex_operations import manage_complex_queries
from crudoperations import manage_basic_crud_operations
from menus import table_list
from db import create_connection

def start_application():
    """
    Entry point for the application.
    Establishes database connection and allows users to perform CRUD operations
    on various entities through a menu-driven interface and explore complex SQL queries.
    """
    # Establish a connection to the database
    conn = create_connection()
    if not conn:
        print("❌ Unable to connect to the database. Exiting...")
        return

    # Continuously display the main menu until the user chooses to exit
    while True:
        table_choice = table_list()

        # Basic CRUD Operations
        if table_choice == "1":
            print("🔄 Accessing Basic CRUD Operations...")
            manage_basic_crud_operations(conn)
        
        # Advanced SQL Queries Section
        elif table_choice == "2":
            print("🔍 Accessing Complex SQL Queries...")
            manage_complex_queries(conn)  # Manage complex SQL queries (Deliverable 5 focus)

        # Exit the application
        elif table_choice == "3":
            print("👋 Exiting... Have a great day!")
            conn.close()
            break

        # Error Handling for Invalid Option
        else:
            print("⚠️ Invalid option, please choose again.")


if __name__ == "__main__":
    start_application()
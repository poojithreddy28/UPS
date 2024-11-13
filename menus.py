def table_list():
    """
    Display the main menu for the UPS Management System and prompt the user to select an option.
    """
    print("\n" + "=" * 50)
    print(f"\033[1m📦 WELCOME TO UPS MANAGEMENT SYSTEM 📦\033[0m".center(50))
    print("Efficiently manage your users, customers, shipments, packages, and payments.".center(50))
    print("Seamlessly handle your logistics with our intuitive interface.".center(50))
    print("=" * 50)
    print("\n\033[1m🗂️ MAIN MENU\033[0m".center(50))
    print("-" * 50)
    print("1. 🗂️ Basic CRUD Operations")  # New section for CRUD operations
    print("2. 📊 Manage Complex SQL Queries")  # New section for complex SQL queries
    print("3. ❌ Exit Application")
    print("=" * 50)
    return input("👉 Select an option (1-3): ").strip()


def crud_operation_menu(entity_name):
    """
    Generate a CRUD operation menu based on the provided entity name and prompt the user to select an action.
    """
    # Users management options
    if entity_name == "Users":
        print("\n" + "=" * 50)
        print(f"\033[1m👤 USER MANAGEMENT OPERATIONS\033[0m".center(50))
        print("-" * 50)
        print("1. ➕ Add New User")
        print("2. 📖 View User Records")
        print("3. ✏️ Edit User Information")
        print("4. ❌ Remove User")
        print("5. 🔙 Return to Main Menu")
        print("=" * 50)
        return input("👉 Choose an option (1-5): ").strip()

    # Customers management options
    elif entity_name == "Customers":
        print("\n" + "=" * 50)
        print(f"\033[1m👥 CUSTOMER MANAGEMENT OPERATIONS\033[0m".center(50))
        print("-" * 50)
        print("1. ➕ Register New Customer")
        print("2. 📖 Access Customer Records")
        print("3. ✏️ Update Customer Profile")
        print("4. ❌ Delete Customer Account")
        print("5. 🔙 Return to Main Menu")
        print("=" * 50)
        return input("👉 Choose an option (1-5): ").strip()

    # Shipments management options
    elif entity_name == "Shipments":
        print("\n" + "=" * 50)
        print(f"\033[1m🚚 SHIPMENT MANAGEMENT OPERATIONS\033[0m".center(50))
        print("-" * 50)
        print("1. ➕ Create New Shipment")
        print("2. 📖 Track Shipment Details")
        print("3. ✏️ Modify Shipment Information")
        print("4. ❌ Cancel Shipment")
        print("5. 🔙 Return to Main Menu")
        print("=" * 50)
        return input("👉 Choose an option (1-5): ").strip()

    # Packages management options
    elif entity_name == "Packages":
        print("\n" + "=" * 50)
        print(f"\033[1m📦 PACKAGE MANAGEMENT OPERATIONS\033[0m".center(50))
        print("-" * 50)
        print("1. ➕ Add New Package")
        print("2. 📖 Check Package Records")
        print("3. ✏️ Edit Package Details")
        print("4. ❌ Remove Package")
        print("5. 🔙 Return to Main Menu")
        print("=" * 50)
        return input("👉 Choose an option (1-5): ").strip()

    # Payments management options
    elif entity_name == "Payments":
        print("\n" + "=" * 50)
        print(f"\033[1m💳 PAYMENT MANAGEMENT OPERATIONS\033[0m".center(50))
        print("-" * 50)
        print("1. ➕ Process New Payment")
        print("2. 📖 Review Payment History")
        print("3. ✏️ Update Payment Information")
        print("4. ❌ Revoke Payment")
        print("5. 🔙 Return to Main Menu")
        print("=" * 50)
        return input("👉 Choose an option (1-5): ").strip()

    # Addresses management options
    elif entity_name == "Addresses":
        print("\n" + "=" * 50)
        print(f"\033[1m🏠 ADDRESS MANAGEMENT OPERATIONS\033[0m".center(50))
        print("-" * 50)
        print("1. ➕ Add New Address")
        print("2. 📖 View Address Records")
        print("3. ✏️ Edit Address Information")
        print("4. ❌ Delete Address")
        print("5. 🔙 Return to Main Menu")
        print("=" * 50)
        return input("👉 Choose an option (1-5): ").strip()

    # Delivery Attempts management options
    elif entity_name == "Delivery Attempts":
        print("\n" + "=" * 50)
        print(f"\033[1m🕵️‍♂️ DELIVERY ATTEMPT MANAGEMENT\033[0m".center(50))
        print("-" * 50)
        print("1. ➕ Log New Attempt")
        print("2. 📖 Review Attempt Records")
        print("3. ✏️ Update Attempt Details")
        print("4. ❌ Remove Attempt Record")
        print("5. 🔙 Return to Main Menu")
        print("=" * 50)
        return input("👉 Choose an option (1-5): ").strip()

    # Package Dimensions management options
    elif entity_name == "Package Dimensions":
        print("\n" + "=" * 50)
        print(f"\033[1m📏 PACKAGE DIMENSIONS OPERATIONS\033[0m".center(50))
        print("-" * 50)
        print("1. ➕ Register Package Dimensions")
        print("2. 📖 Access Dimension Records")
        print("3. ✏️ Adjust Package Dimensions")
        print("4. ❌ Remove Dimension Data")
        print("5. 🔙 Return to Main Menu")
        print("=" * 50)
        return input("👉 Choose an option (1-5): ").strip()

    # Package Status management options
    elif entity_name == "Package Status":
        print("\n" + "=" * 50)
        print(f"\033[1m📄 PACKAGE STATUS OPERATIONS\033[0m".center(50))
        print("-" * 50)
        print("1. ➕ Log New Status")
        print("2. 📖 Check Status History")
        print("3. ✏️ Update Status Entry")
        print("4. ❌ Remove Status Record")
        print("5. 🔙 Return to Main Menu")
        print("=" * 50)
        return input("👉 Choose an option (1-5): ").strip()

    # Pickup Requests management options
    elif entity_name == "Pickup Requests":
        print("\n" + "=" * 50)
        print(f"\033[1m📋 PICKUP REQUEST OPERATIONS\033[0m".center(50))
        print("-" * 50)
        print("1. ➕ Register Pickup Request")
        print("2. 📖 View Pickup Records")
        print("3. ✏️ Edit Pickup Information")
        print("4. ❌ Delete Pickup Request")
        print("5. 🔙 Return to Main Menu")
        print("=" * 50)
        return input("👉 Choose an option (1-5): ").strip()

    # User Roles management options
    elif entity_name == "User Roles":
        print("\n" + "=" * 50)
        print(f"\033[1m🔒 USER ROLES MANAGEMENT\033[0m".center(50))
        print("-" * 50)
        print("1. ➕ Add New Role")
        print("2. 📖 View Role Records")
        print("3. ✏️ Update Role Details")
        print("4. ❌ Delete Role")
        print("5. 🔙 Return to Main Menu")
        print("=" * 50)
        return input("👉 Choose an option (1-5): ").strip()

    else:
        # Generic options for unspecified entities
        print("\n" + "=" * 50)
        print(f"\033[1m🔄 {entity_name.upper()} OPERATIONS\033[0m".center(50))
        print("-" * 50)
        print("1. ➕ Add New Record")
        print("2. 📖 Read Existing Records")
        print("3. ✏️ Update Existing Record")
        print("4. ❌ Delete Record")
        print("5. 🔙 Return to Main Menu")
        print("=" * 50)
        return input("👉 Choose an option (1-5): ").strip()

def display_message(msg):
    """
    Display a styled message for the user, typically for confirmations or alerts.
    """
    print("\n" + "=" * 50)
    print(f"\033[1m🟢 {msg}\033[0m".center(50))  # Bold message
    print("=" * 50)
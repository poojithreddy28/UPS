def crud_operation_menu(entity_name):
    print("\n" + "=" * 50)
    print(f"\033[1m🔄 {entity_name.upper()} OPERATIONS\033[0m".center(50))  # Bold subheading
    print("-" * 50)
    print("1. ➕ Add New Record")
    print("2. 📖 Read Existing Records")
    print("3. ✏️ Update Existing Record")
    print("4. ❌ Delete Record")
    print("5. 🔙 Return to Main Menu")
    print("=" * 50)
    return input("👉 Choose an option (1-5): ").strip()

def table_list():
    print("\n" + "=" * 50)
    print(f"\033[1m📦 WELCOME TO UPS MANAGEMENT SYSTEM 📦\033[0m".center(50))  # Bold subheading
    print("Efficiently manage your users, customers, shipments, packages, and payments.".center(50))
    print("Seamlessly handle your logistics with our intuitive interface.".center(50))
    print("=" * 50)
    print("\n\033[1m🗂️ AVAILABLE TABLES TO MANAGE\033[0m".center(50))  # Bold subheading
    print("-" * 50)
    print("1. 🧑‍💻 Manage Users")
    print("2. 👥 Manage Customers")
    print("3. 🚚 Manage Shipments")
    print("4. 📦 Manage Packages")
    print("5. 💳 Manage Payments")
    print("6. ❌ Exit Application")
    print("=" * 50)
    return input("👉 Select a Table to Manage (1-6): ").strip()

def display_message(msg):
    print("\n" + "=" * 50)
    print(f"\033[1m🟢 {msg}\033[0m".center(50))  # Bold message
    print("=" * 50)
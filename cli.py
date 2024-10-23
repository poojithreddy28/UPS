from crudoperations import create_user, get_all_users

def main_menu():
    while True:
        # Display the menu with improved formatting
        print("\n" + "=" * 40)
        print("          UPS MANAGEMENT MENU          ")
        print("=" * 40)
        print("  1. ➡️  Create User")
        print("  2. 📋  View All Users")
        print("  3. ❌  Exit")
        print("=" * 40)

        # Get user input with a prompt
        choice = input("Choose an option (1, 2, 3): ").strip()

        if choice == '1':
            print("\n-- Create a New User --")
            first_name = input("📝 First Name: ").strip()
            last_name = input("📝 Last Name: ").strip()
            email = input("📧 Email: ").strip()
            phone_number = input("📞 Phone Number: ").strip()
            role_id = input("🔑 Role ID: ").strip()
            password = input("🔒 Password: ").strip()

            create_user(first_name, last_name, email, phone_number, role_id, password)
            print("\n✅ User Created Successfully!")

        elif choice == '2':
            print("\n-- Viewing All Users --")
            print("=" * 40)
            get_all_users()
            print("=" * 40)

        elif choice == '3':
            print("\nExiting... Have a great day!")
            break

        else:
            print("\n ⚠️ Invalid Option! Please choose 1, 2, or 3.")

if __name__ == "__main__":
    main_menu()
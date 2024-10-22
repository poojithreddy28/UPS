from crudoperations import create_user, get_all_users

def main_menu():
    while True:
        print("\nUPS Management Menu:")
        print("1. Create User")
        print("2. View All Users")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            first_name = input("First Name: ")
            last_name = input("Last Name: ")
            email = input("Email: ")
            phone_number = input("Phone Number: ")
            role_id = input("Role ID: ")
            password = input("Password: ")
            create_user(first_name, last_name, email, phone_number, role_id, password)
            print("User Created Successfully!")

        elif choice == '2':
            print("Fetching all users...")
            get_all_users()

        elif choice == '3':
            break

        else:
            print("Invalid Option. Please Try Again.")
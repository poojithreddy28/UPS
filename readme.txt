==================================================
                  UPS MANAGEMENT SYSTEM
==================================================

Setup Instructions

Step 1: Unzip Project Files

1. Download and unzip the project folder from Canvas.

Step 2: Database Setup

1. Open MySQL Workbench and connect to your server.
2. Run the ups.sql file to create the database and tables.
3. Import sample data from the ups_data folder.

Step 3: Update Database Connection

Edit db.py with your MySQL credentials:

def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="your_username",
        password="your_password",
        database="ups_db"
    )

Step 4: Install Dependencies

Run the following command:

pip install mysql-connector-python

Step 5: Run Application

Start the program:

python run_app.py

==================================================

Usage

1. Choose an option from the main menu to manage Users, Customers, Shipments, etc.
2. Follow on-screen prompts for CRUD operations.

==================================================
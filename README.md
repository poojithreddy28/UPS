
# UPS Management System

## Setup Instructions

### Step 1: Unzip Project Files
1. Download and unzip the project folder from Canvas.

### Step 2: Database Setup
1. Open MySQL Workbench and connect to your server.
2. Run the `ups.sql` file to create the database and tables.
3. Import sample data from the `ups_data` folder.

### Step 3: Update Database Connection
Edit `db.py` with your MySQL credentials:

```python
def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="your_username",
        password="your_password",
        database="ups_db"
    )
```

### Step 4: Install Dependencies
Run the following command to install required packages:

```bash
pip install mysql-connector-python
```

### Step 5: Run the Application
Start the program by running:

```bash
python run_app.py
```

---

## Usage

1. Choose an option from the main menu to manage entities such as Users, Customers, and Shipments.
2. Follow on-screen prompts for CRUD (Create, Read, Update, Delete) operations.

---


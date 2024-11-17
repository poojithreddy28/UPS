# complex_operations.py

def complex_queries_menu():
    """
    Display the main menu for managing complex SQL queries, offering an interactive and
    user-friendly interface to enhance the experience for the user.
    """
    print("\n" + "=" * 50)
    print(f"\033[1m📊 COMPLEX SQL QUERIES MENU 📊\033[0m".center(50))
    print("Explore advanced SQL queries for UPS data analysis and operational insights.".center(50))
    print("=" * 50)
    print("1. 📊 OLAP Queries - Analyze multidimensional data.")
    print("2. 🪟 Window Function Queries - Perform row-level analysis with ranking, running totals.")
    print("3. 🔀 Set Operations - Combine and compare multiple datasets.")
    print("4. 📋 Set Membership Queries - Identify set inclusion or exclusion relationships.")
    print("5. 🆚 Set Comparison Queries - Compare datasets based on predefined criteria.")
    print("6. 📐 Advanced Aggregate Functions - Use complex aggregation for nuanced analysis.")
    print("7. 📝 Subqueries Using WITH Clause - Organize and optimize complex subquery execution.")
    print("8. 🔙 Return to Main Menu - Exit the complex queries section.")
    print("=" * 50)
    return input("👉 Select a Complex Query to Run (1-8): ").strip()

def manage_complex_queries(conn):
    """
    Main function to handle complex SQL query selection and execution.
    Includes interactive feedback, clear guidance, and robust error handling.
    """
    while True:
        choice = complex_queries_menu()
        
        if choice == "1":
            manage_olap_queries(conn)
        elif choice == "2":
            manage_window_functions(conn)
        elif choice == "3":
            manage_set_operations(conn)
        elif choice == "4":
            manage_set_membership_queries(conn)
        elif choice == "5":
            manage_set_comparison_queries(conn)
        elif choice == "6":
            manage_advanced_aggregate_functions(conn)  
        elif choice == "7":
            manage_with_clause_subqueries(conn) 
        elif choice == "8":
            print("🔙 Returning to Main Menu. Thank you for exploring complex queries.")
            break
        else:
            print("⚠️ Invalid choice. Please select a valid option from 1 to 8.")

def olap_queries_menu():
    """
    Display the menu for selecting specific OLAP queries with clear descriptions.
    """
    print("\n" + "=" * 50)
    print(f"\033[1m📊 OLAP QUERIES MENU 📊\033[0m".center(50))
    print("Choose an OLAP query to gain insights into UPS data:".center(50))
    print("=" * 50)
    print("1. Distribution of Pickup Request Statuses - Shows breakdown by status.")
    print("2. Monthly Payments with Rollup - Summarize payments by customer, year, and month.")
    print("3. Daily Delivery Success Rate - Calculate success rates for daily deliveries.")
    print("4. Customer Shipment Volume with Percentile Rank - Rank customers by shipments.")
    print("5. 🔙 Return to Complex Queries Menu.")
    print("=" * 50)
    return input("👉 Select an OLAP Query to Run (1-5): ").strip()

def manage_olap_queries(conn):
    """
    Handle OLAP query selection and execution with robust error handling and feedback.
    """
    while True:
        choice = olap_queries_menu()
        
        if choice == "1":
            olap_pickup_request_status_distribution(conn)
        elif choice == "2":
            olap_monthly_payments_with_rollup(conn)
        elif choice == "3":
            olap_daily_delivery_success_rate(conn)
        elif choice == "4":
            olap_customer_shipment_volume(conn)
        elif choice == "5":
            print("🔙 Returning to Complex Queries Menu.")
            break
        else:
            print("⚠️ Invalid choice. Please select a valid option from 1 to 5.")

def format_records(headers, rows):
    """
    Formats and displays records in a well-aligned table format with user-friendly presentation.
    
    :param headers: List of column headers
    :param rows: List of tuples containing row data
    """
    col_widths = [max(len(str(item)) for item in col) for col in zip(headers, *rows)]
    row_format = " | ".join(f"{{:<{width}}}" for width in col_widths)
    
    print("\n" + "=" * (sum(col_widths) + 3 * (len(headers) - 1)))
    print(row_format.format(*headers))
    print("-" * (sum(col_widths) + 3 * (len(headers) - 1)))
    
    for row in rows:
        print(row_format.format(*row))
    
    print("=" * (sum(col_widths) + 3 * (len(headers) - 1)))

# OLAP Queries and Error Handling

def olap_pickup_request_status_distribution(conn):
    """
    OLAP query to determine the percentage distribution of pickup request statuses.
    """
    print("\nRunning OLAP Query: Percentage Distribution of Pickup Request Statuses\n")
    
    query = """
    WITH StatusCounts AS (
        SELECT pickup_status, COUNT(*) AS status_count,
        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() AS percentage
        FROM Pickup_Requests
        GROUP BY pickup_status
    )
    SELECT pickup_status, status_count, ROUND(percentage, 2) AS percentage
    FROM StatusCounts
    ORDER BY status_count DESC;
    """
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            if results:
                headers = ["Pickup Status", "Count", "Percentage (%)"]
                format_records(headers, results)
            else:
                print("⚠️ No data found. Ensure pickup requests are recorded in the system.")
    except Exception as e:
        print(f"❌ Error retrieving pickup request status distribution. Check database connection and data: {e}")
    finally:
        conn.commit()

def olap_monthly_payments_with_rollup(conn):
    """
    OLAP query to retrieve payment details by year, month, and customer with rollup.
    """
    print("\nRunning OLAP Query: Payment Totals by Year, Month, and Customer with Rollup\n")
    
    query = """
    SELECT YEAR(p.payment_date) AS Year, MONTH(p.payment_date) AS Month, c.first_name,
    COUNT(p.payment_id) AS TotalPayments, SUM(p.amount) AS TotalAmount
    FROM Payments p
    JOIN Customers c ON p.customer_id = c.customer_id
    GROUP BY YEAR(p.payment_date), MONTH(p.payment_date), c.first_name WITH ROLLUP;
    """
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            if results:
                headers = ["Year", "Month", "Customer", "Payments", "Amount"]
                formatted_results = [
                    (row[0] if row[0] is not None else "Total",
                     row[1] if row[1] is not None else "",
                     row[2] if row[2] is not None else "",
                     row[3], row[4])
                    for row in results
                ]
                format_records(headers, formatted_results)
            else:
                print("⚠️ No payment data found. Ensure there are payments recorded in the database.")
    except Exception as e:
        print(f"❌ Error retrieving payment totals with rollup. Verify database access and data: {e}")
    finally:
        conn.commit()

def olap_daily_delivery_success_rate(conn):
    """
    Calculates the daily delivery success rate by analyzing delivery attempts.
    """
    print("\nRunning OLAP Query: Daily Delivery Success Rate\n")

    query = """
    SELECT
        DATE(attempt_date) AS delivery_date,
        COUNT(*) AS total_attempts,
        SUM(CASE WHEN attempt_status = 'Success' THEN 1 ELSE 0 END) AS successful_attempts,
        ROUND((SUM(CASE WHEN attempt_status = 'Success' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2) AS success_rate
    FROM DeliveryAttempts
    GROUP BY DATE(attempt_date)
    ORDER BY delivery_date;
    """

    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            
            if results:
                headers = ["Date", "Total Attempts", "Successes", "Success Rate (%)"]
                format_records(headers, results)
            else:
                print("⚠️ No delivery attempt data available. Ensure delivery attempts are recorded in the system.")
    except Exception as e:
        print(f"❌ Error calculating daily delivery success rate. Check for data issues or database access errors: {e}")
    finally:
        conn.commit()

def olap_customer_shipment_volume(conn):
    """
    OLAP query to rank customers by shipment volume using ROLLUP.
    """
    print("\nRunning OLAP Query: Customer Shipment Volume with ROLLUP\n")

    query = """
    WITH CustomerShipmentVolume AS (
        SELECT customer_id, COUNT(shipment_id) AS TotalShipments
        FROM Shipments
        GROUP BY customer_id
    )
    SELECT CSV.customer_id,
    CSV.TotalShipments,
    ROUND(PERCENT_RANK() OVER (ORDER BY CSV.TotalShipments DESC), 2) AS ShipmentPercentile
    FROM CustomerShipmentVolume CSV
    ORDER BY ShipmentPercentile;
    """
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            if results:
                headers = ["Customer ID", "Total Shipments", "Percentile"]
                format_records(headers, results)
            else:
                print("⚠️ No shipment data available for customers. Ensure there are shipments associated with customers.")
    except Exception as e:
        print(f"❌ Error retrieving customer shipment volume. Ensure database connectivity and data accuracy: {e}")
    finally:
        conn.commit()
def window_functions_menu():
    """
    Display the menu for selecting specific window function queries with clear descriptions.
    """
    print("\n" + "=" * 50)
    print(f"\033[1m🪟 WINDOW FUNCTIONS MENU 🪟\033[0m".center(50))
    print("Select a window function query to view insights:".center(50))
    print("=" * 50)
    print("1. First and Last Shipment Dates per User")
    print("   ➤ Shows each user's earliest and latest shipment dates to track activity.")
    print("2. Rank Users by Number of Shipments Handled")
    print("   ➤ Ranks users based on the total shipments handled, identifying top contributors.")
    print("3. Percentile Rank of Customers by Shipment Volume")
    print("   ➤ Calculates percentile ranking of customers by their total shipments.")
    print("4. 4-Month Moving Average of Payment Totals")
    print("   ➤ Computes the 4-month moving average of monthly payments, useful for trend analysis.")
    print("5. 🔙 Return to Complex Queries Menu")
    print("   ➤ Go back to the main complex queries menu.")
    print("=" * 50)
    return input("👉 Select a Window Function Query to Run (1-5): ").strip()

def manage_window_functions(conn):
    """
    Handle window function query selection and execution with robust error handling.
    """
    while True:
        choice = window_functions_menu()
        
        if choice == "1":
            window_first_last_shipment_dates(conn)
        elif choice == "2":
            window_rank_users_by_shipments(conn)
        elif choice == "3":
            window_percentile_customer_shipments(conn)
        elif choice == "4":
            window_moving_average_payments(conn)
        elif choice == "5":
            print("🔙 Returning to Complex Queries Menu.")
            break
        else:
            print("⚠️ Invalid choice. Please select a valid option from 1 to 5.")

def window_first_last_shipment_dates(conn):
    """
    Query to find the earliest and latest shipment dates per user using ROW_NUMBER().
    """
    print("\nRunning Window Function Query: First and Last Shipment Dates per User\n")
    
    query = """
    WITH UserShipments AS (
        SELECT u.user_id, u.first_name, u.last_name, s.shipment_date,
               ROW_NUMBER() OVER (PARTITION BY u.user_id ORDER BY s.shipment_date ASC) AS first_shipment_rank,
               ROW_NUMBER() OVER (PARTITION BY u.user_id ORDER BY s.shipment_date DESC) AS last_shipment_rank
        FROM Users u
        JOIN Shipments s ON u.user_id = s.user_id
    )
    SELECT user_id, first_name, last_name,
           MIN(CASE WHEN first_shipment_rank = 1 THEN shipment_date END) AS earliest_shipment_date,
           MAX(CASE WHEN last_shipment_rank = 1 THEN shipment_date END) AS latest_shipment_date
    FROM UserShipments
    GROUP BY user_id, first_name, last_name
    ORDER BY user_id;
    """
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            if results:
                headers = ["User ID", "First Name", "Last Name", "Earliest Shipment Date", "Latest Shipment Date"]
                format_records(headers, results)
            else:
                print("⚠️ No shipment data found for users.")
    except Exception as e:
        print(f"❌ Error retrieving first and last shipment dates: {e}")
    finally:
        conn.commit()

def window_rank_users_by_shipments(conn):
    """
    Query to rank users by the total number of shipments handled using RANK().
    """
    print("\nRunning Window Function Query: Rank Users by Shipments Handled\n")
    
    query = """
    SELECT u.user_id, COUNT(s.shipment_id) AS TotalShipments,
           RANK() OVER (ORDER BY COUNT(s.shipment_id) DESC) AS UserRank
    FROM Users u
    JOIN Shipments s ON u.user_id = s.user_id
    GROUP BY u.user_id;
    """
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            if results:
                headers = ["User ID", "Total Shipments", "Rank"]
                format_records(headers, results)
            else:
                print("⚠️ No shipment data available for ranking users.")
    except Exception as e:
        print(f"❌ Error ranking users by shipments: {e}")
    finally:
        conn.commit()

def window_percentile_customer_shipments(conn):
    """
    Query to calculate percentile rank of customers by shipment volume using PERCENT_RANK().
    """
    print("\nRunning Window Function Query: Percentile Rank of Customers by Shipment Volume\n")
    
    query = """
    WITH CustomerShipmentVolume AS (
        SELECT customer_id, COUNT(shipment_id) AS TotalShipments
        FROM Shipments
        GROUP BY customer_id
    )
    SELECT customer_id, TotalShipments,
           ROUND(PERCENT_RANK() OVER (ORDER BY TotalShipments DESC), 2) AS ShipmentPercentile
    FROM CustomerShipmentVolume
    ORDER BY ShipmentPercentile;
    """
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            if results:
                headers = ["Customer ID", "Total Shipments", "Percentile"]
                format_records(headers, results)
            else:
                print("⚠️ No shipment data found for customers.")
    except Exception as e:
        print(f"❌ Error calculating shipment percentiles: {e}")
    finally:
        conn.commit()

def window_moving_average_payments(conn):
    """
    Calculate the 4-month moving average of the total payment amounts made each month.
    """
    print("\nRunning Window Function Query: 4-Month Moving Average of Payment Totals\n")

    query = """
    SELECT MonthYear,
           AVG(TotalPayments) OVER (ORDER BY MonthYear ROWS BETWEEN 3 PRECEDING AND CURRENT ROW) AS MovingAvgPayments
    FROM (
        SELECT DATE_FORMAT(payment_date, '%Y-%m') AS MonthYear, SUM(amount) AS TotalPayments
        FROM Payments
        GROUP BY MonthYear
    ) AS MonthlyPaymentTotals;
    """
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            if results:
                headers = ["Month-Year", "4-Month Moving Avg Payments"]
                format_records(headers, results)
            else:
                print("⚠️ No payment data found for moving average calculation.")
    except Exception as e:
        print(f"❌ Error calculating 4-month moving average: {e}")
    finally:
        conn.commit()
def manage_set_operations(conn):
    """
    Menu for selecting specific set operation queries.
    Includes clear menu layout, descriptive use cases, and robust error handling for each operation.
    """
    while True:
        print("\n" + "=" * 50)
        print(f"\033[1m🔀 SET OPERATIONS MENU 🔀\033[0m".center(50))
        print("Select a set operation to run:".center(50))
        print("=" * 50)
        print("1. Union: Combine Distinct Cities from Pickup and Delivery Locations")
        print("2. Intersection: Customers with Both 'Pending' and 'Delivered' Shipments")
        print("3. Difference: Customers Who Made Payments But Never Placed Pickup Requests")
        print("4. 🔙 Return to Complex Queries Menu")
        print("=" * 50)
        
        choice = input("👉 Select a Set Operation to Run (1-4): ").strip()

        if choice == "1":
            set_union_cities(conn)
        elif choice == "2":
            set_intersection_pending_delivered_customers(conn)
        elif choice == "3":
            set_difference_payment_no_pickup(conn)
        elif choice == "4":
            print("🔙 Returning to Complex Queries Menu.")
            break
        else:
            print("⚠️ Invalid choice. Please select a valid option from 1 to 4.")

# Set Operation 1: UNION - Combine Distinct Cities from Pickup and Delivery Locations
def set_union_cities(conn):
    """
    Combines all distinct cities from Pickup Requests and Shipments tables.
    Useful for understanding the geographical coverage of the UPS system.
    """
    print("\nRunning Set Operation: Union of Cities from Pickup and Delivery Locations\n")
    
    query = """
    -- Combine distinct cities from Pickup and Delivery locations
    SELECT DISTINCT addr.City AS City 
    FROM Pickup_Requests pr
    JOIN Addresses addr ON pr.customer_id = addr.customer_id
    UNION
    SELECT DISTINCT addr.City AS City
    FROM Shipments sh
    JOIN Addresses addr ON sh.customer_id = addr.customer_id;
    """
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            if results:
                headers = ["City"]
                format_records(headers, results)
            else:
                print("⚠️ No city data found in Pickup or Delivery records.")
    except Exception as e:
        print(f"❌ Error performing UNION operation on cities: {e}")
    finally:
        conn.commit()

# Set Operation 2: INTERSECT - Customers with Both 'Pending' and 'Delivered' Shipments
def set_intersection_pending_delivered_customers(conn):
    """
    Finds customers who have both 'Pending' and 'Delivered' shipments.
    Useful for analyzing customers with diverse shipment statuses.
    """
    print("\nRunning Set Operation: Intersection of Customers with 'Pending' and 'Delivered' Shipments\n")
    
    query = """
    -- Find customers with both 'Pending' and 'Delivered' shipments
    SELECT DISTINCT s.customer_id
    FROM Shipments s
    WHERE s.shipment_status = 'Pending'
    INTERSECT
    SELECT DISTINCT s.customer_id
    FROM Shipments s
    WHERE s.shipment_status = 'Delivered';
    """
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            if results:
                headers = ["Customer ID"]
                format_records(headers, results)
            else:
                print("⚠️ No customers found with both 'Pending' and 'Delivered' shipments.")
    except Exception as e:
        print(f"❌ Error performing INTERSECT operation on customers: {e}")
    finally:
        conn.commit()

# Set Operation 3: EXCEPT - Customers Who Made Payments But Never Placed Pickup Requests
def set_difference_payment_no_pickup(conn):
    """
    Identifies customers who made payments but have not placed any pickup requests.
    Useful for identifying paying customers without associated service usage.
    """
    print("\nRunning Set Operation: Difference - Customers with Payments But No Pickup Requests\n")
    
    query = """
    -- Find customers who made payments but have not placed pickup requests
    SELECT DISTINCT p.customer_id
    FROM Payments p
    EXCEPT
    SELECT DISTINCT pr.customer_id
    FROM Pickup_Requests pr;
    """
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            if results:
                headers = ["Customer ID"]
                format_records(headers, results)
            else:
                print("⚠️ No customers found with payments but no pickup requests.")
    except Exception as e:
        print(f"❌ Error performing EXCEPT operation on customers: {e}")
    finally:
        conn.commit()

# Utility Function for Formatting Records
def format_records(headers, rows):
    """
    Formats and displays records in a well-aligned table format.
    :param headers: List of column headers
    :param rows: List of tuples containing row data
    """
    # Determine the width for each column based on the maximum data length
    col_widths = [max(len(str(item)) for item in col) for col in zip(headers, *rows)]
    
    # Create a format string for each row
    row_format = " | ".join(f"{{:<{width}}}" for width in col_widths)
    
    # Print the header
    print("\n" + "=" * (sum(col_widths) + 3 * (len(headers) - 1)))
    print(row_format.format(*headers))
    print("-" * (sum(col_widths) + 3 * (len(headers) - 1)))
    
    # Print each row with formatted columns
    for row in rows:
        print(row_format.format(*row))
    
    # Print the footer
    print("=" * (sum(col_widths) + 3 * (len(headers) - 1)))
    
def manage_set_membership_queries(conn):
    """
    Handle set membership queries for UPS database management.
    Provides options to query based on membership operations.
    """
    while True:
        print("\n" + "=" * 50)
        print(f"\033[1m📋 SET MEMBERSHIP QUERIES MENU 📋\033[0m".center(50))
        print("Explore membership queries to gain insights into UPS data:".center(50))
        print("=" * 50)
        print("1. Customers with 'Pending' Pickup Requests")
        print("2. Customers with No Shipments")
        print("3. Packages Assigned to Specific Shipments")
        print("4. 🔙 Return to Complex Queries Menu")
        print("=" * 50)

        choice = input("👉 Select a Set Membership Query to Run (1-4): ").strip()

        if choice == "1":
            customers_with_pending_pickups(conn)
        elif choice == "2":
            customers_with_no_shipments(conn)
        elif choice == "3":
            packages_in_specific_shipments(conn)
        elif choice == "4":
            print("🔙 Returning to Complex Queries Menu.")
            break
        else:
            print("⚠️ Invalid choice. Please select a valid option from 1 to 4.")

def customers_with_pending_pickups(conn):
    """
    Query customers with at least one 'Pending' pickup request.
    """
    print("\nRunning Set Membership Query: Customers with 'Pending' Pickup Requests\n")
    
    query = """
    SELECT DISTINCT pr.customer_id, c.first_name, c.last_name
    FROM Pickup_Requests pr
    JOIN Customers c ON pr.customer_id = c.customer_id
    WHERE pr.pickup_status = 'Pending';
    """
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            if results:
                headers = ["Customer ID", "First Name", "Last Name"]
                col_widths = [max(len(str(item)) for item in col) for col in zip(headers, *results)]
                row_format = " | ".join(f"{{:<{width}}}" for width in col_widths)
                
                print("\n" + "=" * (sum(col_widths) + 3 * (len(headers) - 1)))
                print(row_format.format(*headers))
                print("-" * (sum(col_widths) + 3 * (len(headers) - 1)))
                
                for row in results:
                    print(row_format.format(*row))
                
                print("=" * (sum(col_widths) + 3 * (len(headers) - 1)))
            else:
                print("⚠️ No customers with pending pickup requests.")
    except Exception as e:
        print(f"❌ Error retrieving customers with pending pickups: {e}")
    finally:
        conn.commit()

def customers_with_no_shipments(conn):
    """
    Query customers who have no recorded shipments.
    """
    print("\nRunning Set Membership Query: Customers with No Shipments\n")
    
    query = """
    SELECT DISTINCT c.customer_id, c.first_name, c.last_name
    FROM Customers c
    WHERE c.customer_id NOT IN (
        SELECT DISTINCT s.customer_id
        FROM Shipments s
    );
    """
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            if results:
                headers = ["Customer ID", "First Name", "Last Name"]
                col_widths = [max(len(str(item)) for item in col) for col in zip(headers, *results)]
                row_format = " | ".join(f"{{:<{width}}}" for width in col_widths)
                
                print("\n" + "=" * (sum(col_widths) + 3 * (len(headers) - 1)))
                print(row_format.format(*headers))
                print("-" * (sum(col_widths) + 3 * (len(headers) - 1)))
                
                for row in results:
                    print(row_format.format(*row))
                
                print("=" * (sum(col_widths) + 3 * (len(headers) - 1)))
            else:
                print("⚠️ All customers have shipments.")
    except Exception as e:
        print(f"❌ Error retrieving customers with no shipments: {e}")
    finally:
        conn.commit()

def packages_in_specific_shipments(conn):
    """
    Query packages assigned to specific shipments.
    """
    print("\nRunning Set Membership Query: Packages Assigned to Specific Shipments\n")
    
    shipment_ids = input("Enter comma-separated Shipment IDs: ").strip()
    query = f"""
    SELECT p.package_id, p.contents_description, p.weight
    FROM Packages p
    WHERE p.shipment_id IN ({shipment_ids});
    """
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            if results:
                headers = ["Package ID", "Description", "Weight (kg)"]
                col_widths = [max(len(str(item)) for item in col) for col in zip(headers, *results)]
                row_format = " | ".join(f"{{:<{width}}}" for width in col_widths)
                
                print("\n" + "=" * (sum(col_widths) + 3 * (len(headers) - 1)))
                print(row_format.format(*headers))
                print("-" * (sum(col_widths) + 3 * (len(headers) - 1)))
                
                for row in results:
                    print(row_format.format(*row))
                
                print("=" * (sum(col_widths) + 3 * (len(headers) - 1)))
            else:
                print("⚠️ No packages found for the specified shipments.")
    except Exception as e:
        print(f"❌ Error retrieving packages for specific shipments: {e}")
    finally:
        conn.commit()



def manage_set_comparison_queries(conn):
    """
    Handle set comparison queries for UPS database management.
    Provides options to compare datasets based on specific criteria.
    """
    while True:
        print("\n" + "=" * 50)
        print(f"\033[1m🆚 SET COMPARISON QUERIES MENU 🆚\033[0m".center(50))
        print("Compare datasets to gain insights into UPS operations:".center(50))
        print("=" * 50)
        print("1. Customers with Pickup and Delivery Records")
        print("2. Packages with Consignment and Delivery Information")
        print("3. Users Associated with Multiple Shipments")
        print("4. 🔙 Return to Complex Queries Menu")
        print("=" * 50)

        choice = input("👉 Select a Set Comparison Query to Run (1-4): ").strip()

        if choice == "1":
            customers_with_pickup_and_delivery(conn)
        elif choice == "2":
            packages_with_consignment_delivery_info(conn)
        elif choice == "3":
            users_with_multiple_shipments(conn)
        elif choice == "4":
            print("🔙 Returning to Complex Queries Menu.")
            break
        else:
            print("⚠️ Invalid choice. Please select a valid option from 1 to 4.")

def customers_with_pickup_and_delivery(conn):
    """
    Query customers with both pickup and delivery records.
    """
    print("\nRunning Set Comparison Query: Customers with Pickup and Delivery Records\n")
    
    query = """
    SELECT DISTINCT pr.customer_id, c.first_name, c.last_name
    FROM Pickup_Requests pr
    JOIN Shipments s ON pr.customer_id = s.customer_id
    JOIN Customers c ON pr.customer_id = c.customer_id;
    """
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            if results:
                headers = ["Customer ID", "First Name", "Last Name"]
                col_widths = [max(len(str(item)) for item in col) for col in zip(headers, *results)]
                row_format = " | ".join(f"{{:<{width}}}" for width in col_widths)
                
                print("\n" + "=" * (sum(col_widths) + 3 * (len(headers) - 1)))
                print(row_format.format(*headers))
                print("-" * (sum(col_widths) + 3 * (len(headers) - 1)))
                
                for row in results:
                    print(row_format.format(*row))
                
                print("=" * (sum(col_widths) + 3 * (len(headers) - 1)))
            else:
                print("⚠️ No customers found with both pickup and delivery records.")
    except Exception as e:
        print(f"❌ Error retrieving customers with pickup and delivery records: {e}")
    finally:
        conn.commit()

def packages_with_consignment_delivery_info(conn):
    """
    Query packages with both consignment and delivery information.
    """
    print("\nRunning Set Comparison Query: Packages with Consignment and Delivery Information\n")
    
    query = """
    SELECT DISTINCT p.package_id, p.contents_description, p.weight, ps.status_type
    FROM Packages p
    JOIN PackageStatus ps ON p.package_id = ps.package_id;
    """
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            if results:
                headers = ["Package ID", "Description", "Weight (kg)", "Status Type"]
                col_widths = [max(len(str(item)) for item in col) for col in zip(headers, *results)]
                row_format = " | ".join(f"{{:<{width}}}" for width in col_widths)
                
                print("\n" + "=" * (sum(col_widths) + 3 * (len(headers) - 1)))
                print(row_format.format(*headers))
                print("-" * (sum(col_widths) + 3 * (len(headers) - 1)))
                
                for row in results:
                    print(row_format.format(*row))
                
                print("=" * (sum(col_widths) + 3 * (len(headers) - 1)))
            else:
                print("⚠️ No packages with consignment and delivery information.")
    except Exception as e:
        print(f"❌ Error retrieving packages with consignment and delivery information: {e}")
    finally:
        conn.commit()

def users_with_multiple_shipments(conn):
    """
    Query users associated with multiple shipments.
    """
    print("\nRunning Set Comparison Query: Users Associated with Multiple Shipments\n")
    
    query = """
    SELECT u.user_id, u.first_name, u.last_name, COUNT(s.shipment_id) AS ShipmentCount
    FROM Users u
    JOIN Shipments s ON u.user_id = s.user_id
    GROUP BY u.user_id
    HAVING COUNT(s.shipment_id) > 1;
    """
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            if results:
                headers = ["User ID", "First Name", "Last Name", "Number of Shipments"]
                col_widths = [max(len(str(item)) for item in col) for col in zip(headers, *results)]
                row_format = " | ".join(f"{{:<{width}}}" for width in col_widths)
                
                print("\n" + "=" * (sum(col_widths) + 3 * (len(headers) - 1)))
                print(row_format.format(*headers))
                print("-" * (sum(col_widths) + 3 * (len(headers) - 1)))
                
                for row in results:
                    print(row_format.format(*row))
                
                print("=" * (sum(col_widths) + 3 * (len(headers) - 1)))
            else:
                print("⚠️ No users found with multiple shipments.")
    except Exception as e:
        print(f"❌ Error retrieving users with multiple shipments: {e}")
    finally:
        conn.commit()

def manage_advanced_aggregate_functions(conn):
    """
    Placeholder function for managing advanced aggregate functions.
    This will enable usage of complex aggregations like statistical calculations.
    """
    while True:
        print("\n" + "=" * 50)
        print(f"\033[1m📊 ADVANCED AGGREGATE FUNCTIONS MENU 📊\033[0m".center(50))
        print("Select an advanced aggregation query:".center(50))
        print("=" * 50)
        print("1. Calculate Percentiles of Shipment Weights")
        print("2. Compute Moving Average of Daily Shipment Volumes")
        print("3. Determine Median Payment Amount per Customer")
        print("4. Analyze Shipment Frequency Distribution")
        print("5. Calculate Correlation: Package Dimensions vs Shipping Cost")
        print("6. 🔙 Return to Complex Queries Menu")
        print("=" * 50)
        
        choice = input("👉 Select an option (1-6): ").strip()
        
        if choice == "1":
            calculate_shipment_weight_percentiles(conn)
        elif choice == "2":
            compute_moving_average_shipments(conn)
        elif choice == "3":
            determine_median_payment(conn)
        elif choice == "4":
            analyze_shipment_frequency(conn)
        elif choice == "5":
            print("🔙 Returning to Complex Queries Menu.")
            break
        else:
            print("⚠️ Invalid choice. Please select a valid option from 1 to 6.")


def calculate_shipment_weight_percentiles(conn):
    print("\nCalculating Percentiles of Shipment Weights...")
    query = """
    WITH WeightRanks AS (
        SELECT weight, PERCENT_RANK() OVER (ORDER BY weight) AS percentile
        FROM Packages
    )
    SELECT 
        ROUND(MIN(CASE WHEN percentile >= 0.25 THEN weight END), 2) AS '25th_Percentile',
        ROUND(MIN(CASE WHEN percentile >= 0.50 THEN weight END), 2) AS '50th_Percentile',
        ROUND(MIN(CASE WHEN percentile >= 0.75 THEN weight END), 2) AS '75th_Percentile',
        ROUND(MIN(CASE WHEN percentile >= 0.90 THEN weight END), 2) AS '90th_Percentile'
    FROM WeightRanks;
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
            if result:
                print("\nShipment Weight Percentiles:")
                print(f"25th Percentile: {result[0]} kg")
                print(f"50th Percentile (Median): {result[1]} kg")
                print(f"75th Percentile: {result[2]} kg")
                print(f"90th Percentile: {result[3]} kg")
            else:
                print("No data available for shipment weight percentiles.")
    except Exception as e:
        print(f"Error calculating shipment weight percentiles: {e}")

def compute_moving_average_shipments(conn):
    print("\nComputing 7-Day Moving Average of Daily Shipment Volumes...")
    query = """
    WITH DailyShipments AS (
        SELECT DATE(shipment_date) AS ship_date, COUNT(*) AS daily_count
        FROM Shipments
        GROUP BY DATE(shipment_date)
    )
    SELECT 
        ship_date,
        daily_count,
        AVG(daily_count) OVER (
            ORDER BY ship_date
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) AS moving_average
    FROM DailyShipments
    ORDER BY ship_date DESC
    LIMIT 30;
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            if results:
                print("\nLast 30 days of 7-Day Moving Average of Shipment Volumes:")
                print("Date".ljust(15) + "Daily Count".ljust(15) + "Moving Average")
                print("-" * 45)
                for row in results:
                    print(f"{row[0].strftime('%Y-%m-%d').ljust(15)}{str(row[1]).ljust(15)}{row[2]:.2f}")
            else:
                print("No data available for shipment volume moving average.")
    except Exception as e:
        print(f"Error computing moving average of shipments: {e}")

def determine_median_payment(conn):
    print("\nDetermining Median Payment Amount per Customer...")
    query = """
    WITH CustomerPayments AS (
        SELECT customer_id, amount,
            ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY amount) AS row_num,
            COUNT(*) OVER (PARTITION BY customer_id) AS count
        FROM Payments
    )
    SELECT 
        customer_id,
        AVG(amount) AS median_payment
    FROM CustomerPayments
    WHERE 
        row_num IN (FLOOR((count + 1)/2), CEIL((count + 1)/2))
    GROUP BY customer_id
    ORDER BY median_payment DESC
    LIMIT 10;
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            if results:
                print("\nTop 10 Customers by Median Payment Amount:")
                print("Customer ID".ljust(15) + "Median Payment")
                print("-" * 30)
                for row in results:
                    print(f"{str(row[0]).ljust(15)}${row[1]:.2f}")
            else:
                print("No data available for median payment calculation.")
    except Exception as e:
        print(f"Error determining median payment: {e}")

def analyze_shipment_frequency(conn):
    print("\nAnalyzing Shipment Frequency Distribution...")
    query = """
    WITH CustomerShipments AS (
        SELECT 
            customer_id,
            COUNT(*) AS shipment_count
        FROM Shipments
        GROUP BY customer_id
    )
    SELECT 
        CASE 
            WHEN shipment_count BETWEEN 1 AND 5 THEN '1-5'
            WHEN shipment_count BETWEEN 6 AND 10 THEN '6-10'
            WHEN shipment_count BETWEEN 11 AND 20 THEN '11-20'
            WHEN shipment_count > 20 THEN '20+'
        END AS shipment_range,
        COUNT(*) AS customer_count,
        ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS percentage
    FROM CustomerShipments
    GROUP BY 
        CASE 
            WHEN shipment_count BETWEEN 1 AND 5 THEN '1-5'
            WHEN shipment_count BETWEEN 6 AND 10 THEN '6-10'
            WHEN shipment_count BETWEEN 11 AND 20 THEN '11-20'
            WHEN shipment_count > 20 THEN '20+'
        END
    ORDER BY 
        CASE shipment_range
            WHEN '1-5' THEN 1
            WHEN '6-10' THEN 2
            WHEN '11-20' THEN 3
            WHEN '20+' THEN 4
        END;
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            if results:
                print("\nShipment Frequency Distribution:")
                print("Shipment Range".ljust(20) + "Customer Count".ljust(20) + "Percentage")
                print("-" * 60)
                for row in results:
                    print(f"{row[0].ljust(20)}{str(row[1]).ljust(20)}{row[2]}%")
            else:
                print("No data available for shipment frequency analysis.")
    except Exception as e:
        print(f"Error analyzing shipment frequency: {e}")

def manage_with_clause_subqueries(conn):
    """
    Placeholder function for managing subqueries using the WITH clause.
    This feature will support using WITH for reusable subquery definitions.
    """
    while True:
        print("\n" + "=" * 50)
        print(f"\033[1m📊 WITH CLAUSE SUBQUERIES MENU 📊\033[0m".center(50))
        print("Select a query to run:".center(50))
        print("=" * 50)
        print("1. Analyze Customer Shipment Patterns")
        print("2. Calculate Package Delivery Efficiency")
        print("3. Identify Top-Performing Delivery Personnel")
        print("4. Examine Payment Trends Over Time")
        print("5. Analyze Pickup Request Patterns")
        print("6. 🔙 Return to Complex Queries Menu")
        print("=" * 50)
        
        choice = input("👉 Select an option (1-6): ").strip()
        
        if choice == "1":
            analyze_customer_shipment_patterns(conn)
        elif choice == "2":
            calculate_package_delivery_efficiency(conn)
        elif choice == "3":
            identify_top_performing_personnel(conn)
        elif choice == "4":
            examine_payment_trends(conn)
        elif choice == "5":
            analyze_pickup_request_patterns(conn)
        elif choice == "6":
            print("🔙 Returning to Complex Queries Menu.")
            break
        else:
            print("⚠️ Invalid choice. Please select a valid option from 1 to 6.")

def analyze_customer_shipment_patterns(conn):
    print("\nAnalyzing Customer Shipment Patterns...")
    query = """
    WITH CustomerShipments AS (
        SELECT 
            c.customer_id,
            c.first_name,
            c.last_name,
            COUNT(s.shipment_id) AS total_shipments,
            AVG(p.weight) AS avg_package_weight,
            SUM(CASE WHEN s.shipment_type = 'Express' THEN 1 ELSE 0 END) AS express_shipments
        FROM Customers c
        JOIN Shipments s ON c.customer_id = s.customer_id
        JOIN Packages p ON s.shipment_id = p.shipment_id
        GROUP BY c.customer_id, c.first_name, c.last_name
    )
    SELECT 
        customer_id,
        CONCAT(first_name, ' ', last_name) AS customer_name,
        total_shipments,
        ROUND(avg_package_weight, 2) AS avg_package_weight,
        express_shipments,
        ROUND(express_shipments * 100.0 / total_shipments, 2) AS express_percentage
    FROM CustomerShipments
    ORDER BY total_shipments DESC
    LIMIT 10;
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            if results:
                print("\nTop 10 Customers by Shipment Patterns:")
                headers = ["Customer ID", "Name", "Total Shipments", "Avg Weight (kg)", "Express Shipments", "Express %"]
                format_records(headers, results)
            else:
                print("No data available for customer shipment patterns.")
    except Exception as e:
        print(f"Error analyzing customer shipment patterns: {e}")

def calculate_package_delivery_efficiency(conn):
    print("\nCalculating Package Delivery Efficiency...")
    query = """
    WITH DeliveryStats AS (
        SELECT 
            s.shipment_id,
            s.shipment_date,
            MAX(CASE WHEN da.attempt_status = 'Delivered' THEN da.attempt_date END) AS delivery_date,
            COUNT(da.attempt_id) AS delivery_attempts
        FROM Shipments s
        LEFT JOIN DeliveryAttempts da ON s.shipment_id = da.shipment_id
        GROUP BY s.shipment_id, s.shipment_date
    )
    SELECT 
        AVG(DATEDIFF(delivery_date, shipment_date)) AS avg_delivery_days,
        AVG(delivery_attempts) AS avg_delivery_attempts,
        SUM(CASE WHEN delivery_date IS NOT NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS successful_delivery_percentage
    FROM DeliveryStats;
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
            if result:
                avg_delivery_days = result[0] if result[0] is not None else "N/A"
                avg_delivery_attempts = result[1] if result[1] is not None else "N/A"
                successful_delivery_percentage = result[2] if result[2] is not None else "N/A"
                
                print("\nPackage Delivery Efficiency Metrics:")
                print(f"Average Delivery Time: {avg_delivery_days} days")
                print(f"Average Delivery Attempts: {avg_delivery_attempts}")
                print(f"Successful Delivery Percentage: {successful_delivery_percentage}%")
            else:
                print("No data available for package delivery efficiency calculation.")
    except Exception as e:
        print(f"❌ Error calculating package delivery efficiency: {e}")
    finally:
        conn.commit()

def identify_top_performing_personnel(conn):
    print("\nIdentifying Top-Performing Delivery Personnel...")
    query = """
    WITH PersonnelPerformance AS (
        SELECT 
            u.user_id,
            CONCAT(u.first_name, ' ', u.last_name) AS employee_name,
            COUNT(s.shipment_id) AS total_shipments,
            AVG(CASE WHEN da.attempt_status = 'Delivered' THEN 1 ELSE 0 END) AS delivery_success_rate,
            AVG(DATEDIFF(da.attempt_date, s.shipment_date)) AS avg_delivery_time
        FROM Users u
        JOIN Shipments s ON u.user_id = s.user_id
        LEFT JOIN DeliveryAttempts da ON s.shipment_id = da.shipment_id
        WHERE u.role_id = (SELECT role_id FROM User_Role WHERE role_name = 'Delivery Personnel')
        GROUP BY u.user_id, u.first_name, u.last_name
    )
    SELECT 
        employee_name,
        total_shipments,
        ROUND(delivery_success_rate * 100, 2) AS success_rate_percentage,
        ROUND(avg_delivery_time, 1) AS avg_delivery_days
    FROM PersonnelPerformance
    ORDER BY delivery_success_rate DESC, total_shipments DESC
    LIMIT 10;
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            if results:
                print("\nTop 10 Performing Delivery Personnel:")
                headers = ["Employee Name", "Total Shipments", "Success Rate (%)", "Avg Delivery Time (days)"]
                format_records(headers, results)
            else:
                print("No data available for delivery personnel performance.")
    except Exception as e:
        print(f"Error identifying top-performing personnel: {e}")

def examine_payment_trends(conn):
    print("\nExamining Payment Trends Over Time...")
    query = """
    WITH MonthlyPayments AS (
        SELECT 
            DATE_FORMAT(payment_date, '%Y-%m') AS payment_month,
            SUM(amount) AS total_amount,
            COUNT(*) AS payment_count
        FROM Payments
        GROUP BY DATE_FORMAT(payment_date, '%Y-%m')
    )
    SELECT 
        payment_month,
        total_amount,
        payment_count,
        AVG(total_amount) OVER (ORDER BY payment_month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS moving_avg
    FROM MonthlyPayments
    ORDER BY payment_month DESC
    LIMIT 12;
    """
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            if results:
                print("\nPayment Trends (Last 12 Months):")
                headers = ["Month", "Total Amount", "Payment Count", "3-Month Avg"]
                formatted_results = [
                    (
                        row[0],
                        f"${row[1]:.2f}" if row[1] is not None else "N/A",
                        str(row[2]) if row[2] is not None else "N/A",
                        f"${row[3]:.2f}" if row[3] is not None else "N/A"
                    )
                    for row in results
                ]
                format_records(headers, formatted_results)
            else:
                print("No payment trend data available.")
    except Exception as e:
        print(f"Error examining payment trends: {e}")
    finally:
        conn.commit()

def analyze_pickup_request_patterns(conn):
    print("\nAnalyzing Pickup Request Patterns...")
    query = """
    WITH PickupStats AS (
        SELECT 
            DAYNAME(pickup_date) AS day_of_week,
            HOUR(pickup_date) AS hour_of_day,
            COUNT(*) AS request_count
        FROM Pickup_Requests
        GROUP BY DAYNAME(pickup_date), HOUR(pickup_date)
    ),
    DailyTotals AS (
        SELECT day_of_week, SUM(request_count) AS total_daily_requests
        FROM PickupStats
        GROUP BY day_of_week
    )
    SELECT 
        ps.day_of_week,
        ps.hour_of_day,
        ps.request_count,
        ROUND(ps.request_count * 100.0 / dt.total_daily_requests, 2) AS percentage_of_daily_total
    FROM PickupStats ps
    JOIN DailyTotals dt ON ps.day_of_week = dt.day_of_week
    ORDER BY 
        FIELD(ps.day_of_week, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'),
        ps.hour_of_day;
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            if results:
                print("\nPickup Request Patterns by Day and Hour:")
                headers = ["Day of Week", "Hour", "Request Count", "% of Daily Total"]
                format_records(headers, results)
            else:
                print("No data available for pickup request pattern analysis.")
    except Exception as e:
        print(f"Error analyzing pickup request patterns: {e}")

def format_records(headers, rows):
    """Formats and displays records in a well-aligned table format."""
    col_widths = [max(len(str(item)) for item in col) for col in zip(headers, *rows)]
    row_format = " | ".join(f"{{:<{width}}}" for width in col_widths)
    print("\n" + "=" * (sum(col_widths) + 3 * (len(headers) - 1)))
    print(row_format.format(*headers))
    print("-" * (sum(col_widths) + 3 * (len(headers) - 1)))
    for row in rows:
        print(row_format.format(*row))
    print("=" * (sum(col_widths) + 3 * (len(headers) - 1)))
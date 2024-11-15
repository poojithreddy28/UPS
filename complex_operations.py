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
    Placeholder function for managing set membership queries.
    This function will allow querying based on set membership operations.
    """
    print("\n🚧 Set Membership Queries feature is under construction. Please check back later.")

def manage_set_comparison_queries(conn):
    """
    Placeholder function for managing set comparison queries.
    This function will be implemented to allow comparisons between sets.
    """
    print("\n🚧 Set Comparison Queries feature is under construction. Please check back later.")

def manage_advanced_aggregate_functions(conn):
    """
    Placeholder function for managing advanced aggregate functions.
    This will enable usage of complex aggregations like statistical calculations.
    """
    print("\n🚧 Advanced Aggregate Functions feature is under construction. Please check back later.")

def manage_with_clause_subqueries(conn):
    """
    Placeholder function for managing subqueries using the WITH clause.
    This feature will support using WITH for reusable subquery definitions.
    """
    print("\n🚧 Subqueries Using WITH Clause feature is under construction. Please check back later.")
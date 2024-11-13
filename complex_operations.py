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

# Placeholder for additional functions like manage_window_functions, manage_set_operations, etc.
# Each function should contain similar error handling, user interaction, and feedback messages.
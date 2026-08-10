from __future__ import annotations

from typing import Any

import mysql.connector

# Checks if the database is connected
def check_database_connection(db_config: dict[str, Any]) -> tuple[bool, str]:
    try:
        with mysql.connector.connect(**db_config) as conn: # Connects to the database
            with conn.cursor() as cursor:
                cursor.execute("SELECT DATABASE()") # Executes the query to get the current database
                current_db = cursor.fetchone() # Fetches the result of the query
        db_name = current_db[0] if current_db else db_config["database"] # Gets the name of the database
        return True, f"Connected to database: {db_name}" # Returns True if the database is connected and the name of the database
    except mysql.connector.Error as err: # If the database connection fails, return False and the error
        return False, f"Database connection failed: {err}"

# Runs a query using the cursor and returns the columns and rows
def _run_query(cursor, query: str, params: tuple[Any, ...] = ()) -> dict[str, Any]:
    cursor.execute(query, params) # Executes the query with the parameters
    columns = [col[0] for col in cursor.description] if cursor.description else [] # Gets the columns of the query
    return {"columns": columns, "rows": cursor.fetchall()} # Returns the columns and rows of the query

# Gets the room ids and names from the database to populate the dropdown in the reservation form
def get_rooms(db_config: dict[str, Any]) -> tuple[list[dict[str, Any]], str | None]:
    try:
        with mysql.connector.connect(**db_config) as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(
                    "SELECT room_id, room_no, room_name FROM Room ORDER BY room_id"
                )
                return cursor.fetchall(), None
    except mysql.connector.Error as err:
        return [], f"Could not load room ids: {err}"

# Gets the total unpaid fees for a patron using the function in the ddl
def get_unpaid_fee_total(db_config: dict[str, Any], patron_id: int | None) -> tuple[Any, str | None]:
    try:
        with mysql.connector.connect(**db_config) as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(
                    "SELECT get_unpaid_fee_total(%s) AS unpaid_fee_total",
                    (patron_id,),
                )
                row = cursor.fetchone()
                total = row["unpaid_fee_total"] if row else None
                return total or 0, None
    except mysql.connector.Error as err:
        return 0, f"Could not load unpaid fee total: {err}"

# Uses the query to get unpaid fees
def get_patron_unpaid_fee(db_config: dict[str, Any], patron_id: int | None) -> tuple[dict[str, Any] | None, str | None]:
    try:
        with mysql.connector.connect(**db_config) as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(
                    """
                    SELECT
                        p.patron_id,
                        p.first_name,
                        p.last_name,
                        p.email,
                        COUNT(f.fee_id) AS number_of_unpaid_fees,
                        COALESCE(SUM(f.amount), 0) AS total_unpaid_fees
                    FROM Patron p
                    LEFT JOIN Fee f
                        ON p.patron_id = f.patron_id
                       AND LOWER(f.pay_status) = 'unpaid'
                    WHERE p.patron_id = %s
                    GROUP BY
                        p.patron_id,
                        p.first_name,
                        p.last_name,
                        p.email
                    """,
                    (patron_id,),
                )
                return cursor.fetchone(), None
    except mysql.connector.Error as err:
        return None, f"Could not load unpaid fee summary: {err}"

def get_upcoming_reservations(db_config: dict[str, Any], patron_id: int | None) -> tuple[list[dict[str, Any]], str | None]:
    try:
        with mysql.connector.connect(**db_config) as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(
                    """
                    SELECT
                        r.reservation_id,
                        r.patron_id,
                        rm.room_no,
                        r.reservation_date,
                        r.start_time,
                        r.end_time,
                        r.reservation_type,
                        r.reservation_status
                    FROM Reservation r
                    JOIN Room rm
                        ON r.room_id = rm.room_id
                    WHERE r.patron_id = %s
                      AND (
                            r.reservation_date > CURDATE()
                            OR (
                                r.reservation_date = CURDATE()
                                AND r.start_time >= CURTIME()
                            )
                          )
                    ORDER BY r.reservation_date, r.start_time
                    """,
                    (patron_id,),
                )
                return cursor.fetchall(), None
    except mysql.connector.Error as err:
        return [], f"Could not load upcoming reservations: {err}"

# Main function that gets the data for the dashboard based on the role they are logged into'
# Uses the queries from the dml file
def get_role_sections(db_config: dict[str, Any], role: str, patron_id: int | None, staff_id: int | None) -> tuple[list[dict[str, Any]], str | None]:
    patron_queries = [ # Queries for the patron role
        ("Your Patron Profile", "SELECT patron_id, first_name, last_name, email, member_date FROM Patron WHERE patron_id = %s", (patron_id,)),
        ("Your Checkouts", "SELECT c.checkout_date, c.due_date, c.return_date, m.title, m.material_type FROM Checkouts c JOIN Material m ON c.material_id = m.material_id WHERE c.patron_id = %s ORDER BY c.checkout_date DESC", (patron_id,)),
        ("Your Cafe Orders", "SELECT co.orderID, co.orderDate, co.orderPayment, co.staffID FROM CafeOrder co WHERE co.patron_id = %s ORDER BY co.orderDate DESC", (patron_id,)),
        ("Your Fees", "SELECT fee_id, fee_type, amount, fee_date, pay_status FROM Fee WHERE patron_id = %s ORDER BY fee_date DESC", (patron_id,)),
        ("Your Reservations", "SELECT reservation_id, room_id, reservation_date, reservation_type, reservation_status, start_time, end_time FROM Reservation WHERE patron_id = %s ORDER BY reservation_date DESC", (patron_id,)),
        ("Your Event Registrations", "SELECT reg_id, event_id, reg_date, reg_status FROM Registration WHERE patron_id = %s ORDER BY reg_date DESC", (patron_id,)),
    ]
    all_table_queries = [ # Queries for all the tables in the database, for staff and admin
        ("Patron", "SELECT * FROM Patron ORDER BY patron_id LIMIT 100", ()),
        ("Room", "SELECT * FROM Room ORDER BY room_id LIMIT 100", ()),
        ("Reservation", "SELECT * FROM Reservation ORDER BY reservation_id LIMIT 100", ()),
        ("SchoolEvent", "SELECT * FROM SchoolEvent ORDER BY event_id LIMIT 100", ()),
        ("Registration", "SELECT * FROM Registration ORDER BY reg_id LIMIT 100", ()),
        ("Fee", "SELECT * FROM Fee ORDER BY fee_id LIMIT 100", ()),
        ("Material", "SELECT * FROM Material ORDER BY material_id LIMIT 100", ()),
        ("Checkouts", "SELECT * FROM Checkouts ORDER BY checkout_date DESC LIMIT 100", ()),
        ("CheckoutRequest", "SELECT * FROM CheckoutRequest ORDER BY request_date DESC, request_id DESC LIMIT 100", ()),
        ("Author", "SELECT * FROM Author ORDER BY author_id LIMIT 100", ()),
        ("Director", "SELECT * FROM Director ORDER BY director_id LIMIT 100", ()),
        ("Book", "SELECT * FROM Book ORDER BY isbn LIMIT 100", ()),
        ("Book_ISBN_Connector", "SELECT * FROM Book_ISBN_Connector ORDER BY material_id LIMIT 100", ()),
        ("Film", "SELECT * FROM Film ORDER BY imdb_id LIMIT 100", ()),
        ("Film_Connector", "SELECT * FROM Film_Connector ORDER BY material_id LIMIT 100", ()),
        ("Role", "SELECT * FROM Role ORDER BY roleID LIMIT 100", ()),
        ("Staff", "SELECT * FROM Staff ORDER BY staffID LIMIT 100", ()),
        ("Category", "SELECT * FROM Category ORDER BY categoryID LIMIT 100", ()),
        ("CafeItem", "SELECT * FROM CafeItem ORDER BY itemID LIMIT 100", ()),
        ("CafeOrder", "SELECT * FROM CafeOrder ORDER BY orderID DESC LIMIT 100", ()),
        ("OrderItem", "SELECT * FROM OrderItem ORDER BY orderID DESC LIMIT 100", ()),
        ("Availability", "SELECT * FROM Availability ORDER BY availableID LIMIT 100", ()),
        ("Shift", "SELECT * FROM Shift ORDER BY shiftID LIMIT 100", ()),
    ]

    staff_queries = [ # Queries for the staff role
        ("Your Staff Profile", "SELECT s.staffID, s.firstname, s.lastname, s.email, r.roleName, r.hourlyRate FROM Staff s JOIN Role r ON s.roleID = r.roleID WHERE s.staffID = %s", (staff_id,)),
    ] + all_table_queries
    admin_queries = all_table_queries # Queries for the admin role
    selected = patron_queries if role == "patron" else staff_queries if role == "staff" else admin_queries
    try: # Tries to run the queries and return the sections
        with mysql.connector.connect(**db_config) as conn:
            with conn.cursor(dictionary=True) as cursor:
                sections = [] # List to store query results in
                for title, query, params in selected:
                    result = _run_query(cursor, query, params) # Runs the query and returns the columns and rows
                    sections.append({"table_name": title, "columns": result["columns"], "rows": result["rows"]}) # Adds the query results to the list
        return sections, None # Returns the list of query results and None if no error
    except mysql.connector.Error as err:
        return [], f"Could not load dashboard data: {err}" # If the queries fail, return an empty list and the error

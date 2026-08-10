from __future__ import annotations

import os
from datetime import date, timedelta
from functools import wraps
from typing import Any

from flask import Flask, flash, redirect, render_template, request, session, url_for, jsonify
from dotenv import load_dotenv
from db_access import ( # Imports the functions from the db_access.py file
    check_database_connection,
    get_patron_unpaid_fee,
    get_rooms,
    get_upcoming_reservations,
    get_role_sections,
)
import mysql.connector


load_dotenv() # Loads the environment variables from the .env file

app = Flask(__name__, static_folder="static", template_folder="templates") # Creates the Flask app
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key")

# Can add more users here
DEMO_USERS = {
    "patron1": {"password": "patron1", "role": "patron", "patron_id": 1}, # hard coded values for demo
    "patron2": {"password": "patron2", "role": "patron", "patron_id": 2},
    "patron3": {"password": "patron3", "role": "patron", "patron_id": 3},
    "staff1": {"password": "staff1", "role": "staff", "staff_id": 1},
    "staff2": {"password": "staff2", "role": "staff", "staff_id": 2},
    "staff3": {"password": "staff3", "role": "staff", "staff_id": 3},
}


# Makes sure the user is logged in
def _is_logged_in() -> bool:
    return bool(session.get("logged_in"))


# Makes sure the database is connected to your local instance
def _db_config() -> dict[str, Any]:
    return {
        "host": os.environ.get("DB_HOST", "127.0.0.1"),
        "port": int(os.environ.get("DB_PORT", "3306")),
        "user": os.environ.get("DB_USER", "root"),
        "password": os.environ.get("DB_PASSWORD", ""),
        "database": os.environ.get("DB_NAME", "library_database"),
    }

# Helper function to make sure the user is logged in
def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if not _is_logged_in():
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped_view


# The following defines the routes for the website
# Each route returns an html page that is displayed

# Main route that redirects to login
@app.route("/")
def index():
    return redirect(url_for("login"))

# Login route that will get the username and password from the form and check if it is valid
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        account = DEMO_USERS.get(username)

        if not username or not password:
            error = "Please enter both a username and password."
        elif not account or account["password"] != password:
            error = "Invalid username or password."
        else:
            session["logged_in"] = True
            session["username"] = username
            session["role"] = account["role"]
            session["patron_id"] = account.get("patron_id")
            session["staff_id"] = account.get("staff_id")
            return redirect(url_for("dashboard")) # If it is valid, redirect to the dashboard

    return render_template("login.html", error=error) # If it is not valid, show the login page with the error

# Dashboard route that will display the dashboard page
@app.route("/dashboard")
@login_required
def dashboard():
    db_ok, db_message = check_database_connection(_db_config()) # Checks if the database is connected
    preview_data, preview_error = ([], None) # Initializes the preview data and error
    room_options, room_error = ([], None)
    unpaid_fee, unpaid_fee_error = (None, None)
    upcoming_reservations, upcoming_reservations_error = ([], None)

    materials = []
    available_materials = []
    requestable_materials = []
    patron_checkout_requests = []
    active_checkouts = []
    all_checkouts = []
    pending_checkout_requests = []
    checked_out_count = 0

    role = session.get("role", "") # Gets the role of the user

    if db_ok: # If the database is connected, get the preview data
        preview_data, preview_error = get_role_sections( # Gets the preview data for the role based on their patronid or staffid or admin
            _db_config(),
            role=role,
            patron_id=session.get("patron_id"),
            staff_id=session.get("staff_id"),
        )
        try:
            conn = mysql.connector.connect(**_db_config())
            cursor = conn.cursor(dictionary=True)

            if role in ("patron", "staff"):
                cursor.execute("SELECT * FROM Patron_Material_View")
                materials = cursor.fetchall()

            if role == "patron":
                cursor.execute(
                    """
                    SELECT material_id, title, material_type, genre
                    FROM Material
                    WHERE LOWER(material_type) IN ('book', 'film')
                      AND LOWER(availability) = 'available'
                    ORDER BY material_type, title, material_id
                    """
                )
                requestable_materials = cursor.fetchall()
                cursor.execute(
                    """
                    SELECT
                        cr.request_id,
                        cr.request_date,
                        cr.request_status,
                        cr.material_id,
                        m.title,
                        m.material_type
                    FROM CheckoutRequest cr
                    JOIN Material m
                        ON cr.material_id = m.material_id
                    WHERE cr.patron_id = %s
                    ORDER BY cr.request_date DESC, cr.request_id DESC
                    """,
                    (session.get("patron_id"),),
                )
                patron_checkout_requests = cursor.fetchall()

            if role == "staff":
                cursor.execute(
                    """
                    SELECT material_id, title, material_type, genre
                    FROM Material
                    WHERE LOWER(material_type) IN ('book', 'film')
                      AND LOWER(availability) = 'available'
                    ORDER BY material_type, title, material_id
                    """
                )
                available_materials = cursor.fetchall()
                cursor.execute(
                    """
                    SELECT
                        c.patron_id,
                        c.material_id,
                        m.material_type,
                        m.title,
                        c.checkout_date,
                        c.due_date
                    FROM Checkouts c
                    JOIN Material m
                        ON c.material_id = m.material_id
                    WHERE c.return_date IS NULL
                      AND LOWER(m.material_type) IN ('book', 'film')
                    ORDER BY c.due_date, c.patron_id, m.material_type, m.title
                    """
                )
                active_checkouts = cursor.fetchall()
                cursor.execute(
                    """
                    SELECT
                        patron_id,
                        material_id,
                        checkout_date,
                        due_date,
                        return_date
                    FROM Checkouts
                    ORDER BY checkout_date DESC, patron_id, material_id
                    """
                )
                all_checkouts = cursor.fetchall()
                cursor.execute(
                    """
                    SELECT
                        cr.request_id,
                        cr.patron_id,
                        cr.material_id,
                        m.material_type,
                        m.title,
                        cr.request_date,
                        cr.request_status
                    FROM CheckoutRequest cr
                    JOIN Material m
                        ON cr.material_id = m.material_id
                    WHERE cr.request_status = 'pending'
                    ORDER BY cr.request_date, cr.patron_id, m.title
                    """
                )
                pending_checkout_requests = cursor.fetchall()

            cursor.execute("""
                SELECT COUNT(*) AS num_checked_out
                FROM Checkouts c
                JOIN Material m ON c.material_id = m.material_id
                WHERE c.return_date IS NULL;
            """)
            checked_out_count = cursor.fetchone()["num_checked_out"]

            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            print(f"Database error: {err}")

        if role == "patron":
            room_options, room_error = get_rooms(_db_config())
            unpaid_fee, unpaid_fee_error = get_patron_unpaid_fee(
                _db_config(),
                session.get("patron_id"),
            )
            upcoming_reservations, upcoming_reservations_error = get_upcoming_reservations(
                _db_config(),
                session.get("patron_id"),
            )
            preview_error = (
                preview_error
                or room_error
                or unpaid_fee_error
                or upcoming_reservations_error
            )

    return render_template( # Renders the dashboard page with the associated information
        "home.html",
        username=session.get("username"),
        role=role,
        db_ok=db_ok,
        db_message=db_message,
        preview_data=preview_data,
        preview_error=preview_error,
        room_options=room_options,
        unpaid_fee_summary=unpaid_fee,
        upcoming_reservations=upcoming_reservations,

        materials=materials,
        available_materials=available_materials,
        requestable_materials=requestable_materials,
        patron_checkout_requests=patron_checkout_requests,
        active_checkouts=active_checkouts,
        all_checkouts=all_checkouts,
        pending_checkout_requests=pending_checkout_requests,
        default_due_date=(date.today() + timedelta(days=14)).isoformat(),
        min_due_date=(date.today() + timedelta(days=1)).isoformat(),
        checked_out_count=checked_out_count
    )

# Route for browsing library catalogue for books as a patron
@app.route("/searchCatalogueBookTitles", methods=["GET"])
@login_required
def browseCatalogueByFilmTitle():
    title_requested = request.args.get('book_title')
    books_found = []
    print(f"searching for: {title_requested}")

    if title_requested:
        try:
            conn = mysql.connector.connect(**_db_config())
            cursor = conn.cursor(dictionary=True)

            user_input = f"%{title_requested}%"
            db_query = "SELECT m.title, a.first_name, a.last_name, m.genre, b.publisher, m.publish_date, b.page_count, b.isbn, m.availability, m.blurb FROM Book b JOIN Book_ISBN_Connector bc on b.isbn = bc.isbn JOIN Material m on m.material_id = bc.material_id JOIN Author a on b.author_id = a.author_id WHERE m.title LIKE %s"
            cursor.execute(db_query, (user_input,))
            books_found = cursor.fetchall()
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return jsonify([])
        return jsonify(books_found)

# Route for browsing library catalogue for film as a patron
@app.route("/searchCatalogueFilmTitles", methods=["GET"])
@login_required
def browseCatalogueByTitle():
    title_requested = request.args.get('film_title')
    films_found = []
    print(f"searching for: {title_requested}")

    if title_requested:
        try:
            conn = mysql.connector.connect(**_db_config())
            cursor = conn.cursor(dictionary=True)

            user_input = f"%{title_requested}%"
            db_query = "SELECT m.title, d.first_name, d.last_name, f.film_length, m.genre, f.studio, m.publish_date, f.rating, f.film_format, m. availability, m.blurb FROM Film f JOIN Film_Connector fc on f.imdb_id = fc.imdb_id JOIN Material m on m.material_id = fc.material_id JOIN Director d on d.director_id = f.director_id WHERE m.title LIKE %s"
            cursor.execute(db_query, (user_input,))
            films_found = cursor.fetchall()
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return jsonify([])
        return jsonify(films_found)

# Route for updating patron's email information
@app.route('/update_email', methods=['POST'])
@login_required
def update_patron_email():
    patron_id = session.get('patron_id')
    new_email = request.form['new_email']

    if not patron_id:
        return "The patron_id was not found"
    try:
        conn = mysql.connector.connect(**_db_config())
        cursor = conn.cursor(dictionary=True)
        update_email_query = "UPDATE Patron SET email = %s WHERE patron_id = %s"
        cursor.execute(update_email_query, (new_email, patron_id))
        conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.error as err:
        return f"Database error: {err}"

    return redirect(url_for('dashboard'))

# Route for patrons to add a new room reservation
@app.route('/create_reservation', methods=['POST'])
@login_required
def create_reservation():
    if session.get("role") != "patron":
        return redirect(url_for("dashboard"))

    patron_id = session.get('patron_id')
    room_id = request.form.get('room_id')
    reservation_date = request.form.get('reservation_date')
    reservation_type = request.form.get('reservation_type')
    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')

    if not patron_id:
        return "The patron_id was not found"

    try:
        conn = mysql.connector.connect(**_db_config())
        cursor = conn.cursor(dictionary=True)
        insert_reservation_query = """
            INSERT INTO Reservation
                (patron_id, room_id, reservation_date, reservation_type, reservation_status, start_time, end_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(
            insert_reservation_query,
            (
                patron_id,
                room_id,
                reservation_date,
                reservation_type,
                "Pending",
                start_time,
                end_time,
            ),
        )
        conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        flash(f"Reservation could not be added due to a trigger error: {err.msg}", "error")
        return redirect(url_for('dashboard'))

    flash("Reservation added successfully.", "success")

    return redirect(url_for('dashboard'))

# Route for patrons to delete one of their room reservations
@app.route('/delete_reservation', methods=['POST'])
@login_required
def delete_reservation():
    if session.get("role") != "patron":
        return redirect(url_for("dashboard"))

    patron_id = session.get('patron_id')
    reservation_id = request.form.get('reservation_id')

    if not patron_id:
        return "The patron_id was not found"

    if not reservation_id:
        flash("Please enter a reservation ID to delete.", "error")
        return redirect(url_for('dashboard'))

    try:
        conn = mysql.connector.connect(**_db_config())
        cursor = conn.cursor(dictionary=True)
        delete_reservation_query = """
            DELETE FROM Reservation
            WHERE reservation_id = %s
              AND patron_id = %s
        """
        cursor.execute(delete_reservation_query, (reservation_id, patron_id))
        conn.commit()
        deleted_count = cursor.rowcount
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        flash(f"Reservation could not be deleted: {err.msg}", "error")
        return redirect(url_for('dashboard'))

    if deleted_count:
        flash("Reservation deleted successfully.", "success")
    else:
        flash("No matching reservation was found for your account.", "error")

    return redirect(url_for('dashboard'))

@app.route('/request_checkout', methods=['POST'])
@login_required
def request_checkout():
    if session.get("role") != "patron":
        return redirect(url_for("dashboard"))

    patron_id = session.get("patron_id")
    material_id = request.form.get('material_id')

    if not patron_id or not material_id:
        flash("Please choose a material.", "error")
        return redirect(url_for('dashboard'))

    try:
        conn = mysql.connector.connect(**_db_config())
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT material_id, title, material_type, availability
            FROM Material
            WHERE material_id = %s
            """,
            (material_id,),
        )
        material = cursor.fetchone()

        if not material:
            flash("No material was found with that material ID.", "error")
            cursor.close()
            conn.close()
            return redirect(url_for('dashboard'))

        if material["material_type"].lower() not in ("book", "film"):
            flash("Only books and films can be requested.", "error")
            cursor.close()
            conn.close()
            return redirect(url_for('dashboard'))

        if material["availability"].lower() != "available":
            flash("That material is not available to request.", "error")
            cursor.close()
            conn.close()
            return redirect(url_for('dashboard'))

        cursor.execute(
            """
            SELECT 1
            FROM Checkouts
            WHERE patron_id = %s
              AND material_id = %s
              AND return_date IS NULL
            LIMIT 1
            """,
            (patron_id, material_id),
        )
        existing_checkout = cursor.fetchone()

        if existing_checkout:
            flash("You already have an active checkout for that material.", "error")
            cursor.close()
            conn.close()
            return redirect(url_for('dashboard'))

        cursor.execute(
            """
            SELECT 1
            FROM CheckoutRequest
            WHERE patron_id = %s
              AND material_id = %s
              AND request_status = 'pending'
            LIMIT 1
            """,
            (patron_id, material_id),
        )
        existing_request = cursor.fetchone()

        if existing_request:
            flash("You already have a pending request for that material.", "error")
            cursor.close()
            conn.close()
            return redirect(url_for('dashboard'))

        cursor.execute(
            """
            INSERT INTO CheckoutRequest
                (request_date, request_status, patron_id, material_id)
            VALUES (CURDATE(), 'pending', %s, %s)
            """,
            (patron_id, material_id),
        )
        conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        flash(f"Checkout request could not be created: {err.msg}", "error")
        return redirect(url_for('dashboard'))

    flash(f"Checkout request for {material['title']} submitted.", "success")
    return redirect(url_for('dashboard'))

# Route for staff to check out an available book or film for a patron
@app.route('/checkout_book', methods=['POST'])
@app.route('/checkout_material', methods=['POST'])
@login_required
def checkout_material():
    if session.get("role") != "staff":
        return redirect(url_for("dashboard"))

    patron_id = request.form.get('patron_id')
    material_id = request.form.get('material_id')
    due_date = request.form.get('due_date')

    if not patron_id or not material_id or not due_date:
        flash("Please enter a patron ID, choose a material, and choose a due date.", "error")
        return redirect(url_for('dashboard'))

    try:
        conn = mysql.connector.connect(**_db_config())
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT patron_id FROM Patron WHERE patron_id = %s",
            (patron_id,),
        )
        patron = cursor.fetchone()

        if not patron:
            flash("No patron was found with that patron ID.", "error")
            cursor.close()
            conn.close()
            return redirect(url_for('dashboard'))

        cursor.execute(
            """
            SELECT material_id, title, material_type, availability
            FROM Material
            WHERE material_id = %s
            FOR UPDATE
            """,
            (material_id,),
        )
        material = cursor.fetchone()

        if not material:
            flash("No material was found with that material ID.", "error")
            cursor.close()
            conn.close()
            return redirect(url_for('dashboard'))

        if material["material_type"].lower() not in ("book", "film"):
            flash("Only books and films can be checked out with this form.", "error")
            cursor.close()
            conn.close()
            return redirect(url_for('dashboard'))

        if material["availability"].lower() != "available":
            flash("That material is already checked out.", "error")
            cursor.close()
            conn.close()
            return redirect(url_for('dashboard'))

        insert_checkout_query = """
            INSERT INTO Checkouts
                (due_date, return_date, checkout_date, patron_id, material_id)
            VALUES (%s, NULL, CURDATE(), %s, %s)
        """
        cursor.execute(insert_checkout_query, (due_date, patron_id, material_id))
        conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        flash(f"Material could not be checked out: {err.msg}", "error")
        return redirect(url_for('dashboard'))

    flash(f"{material['title']} checked out successfully.", "success")

    return redirect(url_for('dashboard'))

# Route for staff to return a checked out book or film
@app.route('/return_book', methods=['POST'])
@app.route('/return_material', methods=['POST'])
@login_required
def return_material():
    if session.get("role") != "staff":
        return redirect(url_for("dashboard"))

    patron_id = request.form.get('patron_id')
    material_id = request.form.get('material_id')

    if not patron_id or not material_id:
        flash("Please enter both a patron ID and material ID.", "error")
        return redirect(url_for('dashboard'))

    try:
        conn = mysql.connector.connect(**_db_config())
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT c.checkout_date, CURDATE() AS db_today
            FROM Checkouts c
            JOIN Material m
                ON c.material_id = m.material_id
            WHERE c.patron_id = %s
              AND c.material_id = %s
              AND c.return_date IS NULL
              AND LOWER(m.material_type) IN ('book', 'film')
            ORDER BY checkout_date DESC
            LIMIT 1
            """,
            (patron_id, material_id),
        )
        checkout = cursor.fetchone()

        if not checkout:
            cursor.close()
            conn.close()
            flash("No active checkout was found for that patron and material.", "error")
            return redirect(url_for('dashboard'))

        if checkout["checkout_date"] > checkout["db_today"]:
            flash(
                "This material cannot be returned yet because its checkout date is in the future.",
                "error",
            )
            cursor.close()
            conn.close()
            return redirect(url_for('dashboard'))

        update_checkout_query = """
            UPDATE Checkouts
            SET return_date = CURDATE()
            WHERE patron_id = %s
              AND material_id = %s
              AND return_date IS NULL
        """
        cursor.execute(update_checkout_query, (patron_id, material_id))
        conn.commit()
        updated_count = cursor.rowcount
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        flash(f"Material could not be returned: {err.msg}", "error")
        return redirect(url_for('dashboard'))

    if updated_count:
        flash("Material returned successfully.", "success")
    else:
        flash("No active checkout was found for that patron and material.", "error")

    return redirect(url_for('dashboard'))

@app.route('/update_checkout_status', methods=['POST'])
@login_required
def update_checkout_status():
    if session.get("role") != "staff":
        return redirect(url_for("dashboard"))

    request_id = request.form.get('request_id')
    due_date = request.form.get('due_date')
    status = request.form.get('status')

    if not request_id or not status:
        flash("Please choose a pending checkout request and status.", "error")
        return redirect(url_for('dashboard'))

    if status not in ("accepted", "denied"):
        flash("Checkout status must be accepted or denied.", "error")
        return redirect(url_for('dashboard'))

    if status == "accepted" and not due_date:
        flash("Please choose a due date when accepting a checkout request.", "error")
        return redirect(url_for('dashboard'))

    try:
        conn = mysql.connector.connect(**_db_config())
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT
                cr.request_id,
                cr.patron_id,
                cr.material_id,
                m.title,
                m.availability
            FROM CheckoutRequest cr
            JOIN Material m
                ON cr.material_id = m.material_id
            WHERE cr.request_id = %s
              AND cr.request_status = 'pending'
            FOR UPDATE
            """,
            (request_id,),
        )
        checkout_request = cursor.fetchone()

        if not checkout_request:
            cursor.close()
            conn.close()
            flash("No pending checkout request was found.", "error")
            return redirect(url_for('dashboard'))

        if status == "accepted":
            if checkout_request["availability"].lower() != "available":
                cursor.close()
                conn.close()
                flash("That material is no longer available to check out.", "error")
                return redirect(url_for('dashboard'))

            cursor.execute(
                """
                INSERT INTO Checkouts
                    (due_date, return_date, checkout_date, patron_id, material_id)
                VALUES (%s, NULL, CURDATE(), %s, %s)
                """,
                (
                    due_date,
                    checkout_request["patron_id"],
                    checkout_request["material_id"],
                ),
            )

        cursor.execute(
            """
            UPDATE CheckoutRequest
            SET request_status = %s
            WHERE request_id = %s
            """,
            (status, request_id),
        )
        conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        flash(f"Checkout status could not be updated: {err.msg}", "error")
        return redirect(url_for('dashboard'))

    flash(f"Checkout request updated to {status}.", "success")

    return redirect(url_for('dashboard'))

# Route for creating a new patron library account
@app.route('/create_new_patron_account', methods=['POST'])
@login_required
def create_new_patron_account():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    member_date = request.form.get('member_date')
    try:
        conn = mysql.connector.connect(**_db_config())
        cursor = conn.cursor(dictionary=True)
        insert_new_patron_account_query = "INSERT INTO Patron (first_name, last_name, email, member_date) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_new_patron_account_query, (first_name, last_name, email, member_date))
        conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.error as err:
        return f"Database error: {err}"

    return redirect(url_for('dashboard'))

# route for deleting a patron account
@app.route('/delete_patron_account', methods=['POST'])
@login_required
def delete_patron_account():
    account_to_delete = request.form.get('patron_id')

    try:
        conn = mysql.connector.connect(**_db_config())
        cursor = conn.cursor(dictionary=True)
        check_in_deleted_patron_books_query = "UPDATE Material m JOIN Checkouts c ON m.material_id = c.material_id SET m.availability = 'available' WHERE c.patron_id = %s"
        cursor.execute(check_in_deleted_patron_books_query, (account_to_delete,))
        delete_patron_account_query = "DELETE FROM Patron WHERE patron_id = %s"
        cursor.execute(delete_patron_account_query, (account_to_delete,))
        conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.error as err:
        return f"Database error: {err}"

    return redirect(url_for('dashboard'))

# Route for staff to update a pending room reservation status
@app.route('/update_room_reservation', methods=['POST'])
@login_required
def update_room_reservation():
    if session.get("role") not in ["staff", "admin"]:
        return redirect(url_for("dashboard"))

    reservation_id = request.form.get('reservation_id')
    reservation_status = request.form.get('reservation_status')
    allowed_statuses = {"Confirmed", "Denied"}

    if not reservation_id:
        flash("Please enter a reservation ID to update.", "error")
        return redirect(url_for('dashboard'))

    if reservation_status not in allowed_statuses:
        flash("Please choose Confirmed or Denied for the reservation status.", "error")
        return redirect(url_for('dashboard'))

    try:
        conn = mysql.connector.connect(**_db_config())
        cursor = conn.cursor(dictionary=True)
        update_reservation_query = """
            UPDATE Reservation
            SET reservation_status = %s
            WHERE reservation_id = %s
              AND LOWER(reservation_status) = 'pending'
        """
        cursor.execute(update_reservation_query, (reservation_status, reservation_id))
        conn.commit()
        updated_count = cursor.rowcount
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        flash(f"Reservation status could not be updated: {err.msg}", "error")
        return redirect(url_for('dashboard'))

    if updated_count:
        flash("Reservation status updated successfully.", "success")
    else:
        flash("No pending reservation was found with that ID.", "error")

    return redirect(url_for('dashboard'))

# Route for getting emails of patrons with checked out books
@app.route('/get_patron_emails', methods=['GET'])
def get_patrons():
    try:
        conn = mysql.connector.connect(**_db_config())
        cursor = conn.cursor(dictionary=True)
        get_emails_query = "SELECT DISTINCT c.patron_id, p.first_name, p.last_name, p.email FROM Checkouts c JOIN  Patron p on c.patron_id = p.patron_id WHERE c.return_date IS NULL AND c.material_id IN (SELECT m.material_id FROM  Material m WHERE m.availability = 'checked out');"
        cursor.execute(get_emails_query)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
    except mysql.connector.error as err:
        return f"Database error: {err}"
    return jsonify(results)

# Route for staff to update patron's email information
@app.route('/staff_update_patron_email', methods=['POST'])
@login_required
def staff_update_patron_email():
    patron_id = request.form['patron_id']
    new_email = request.form['new_email']

    if not patron_id:
        return "The patron_id was not found"
    try:
        conn = mysql.connector.connect(**_db_config())
        cursor = conn.cursor(dictionary=True)
        update_email_query = "UPDATE Patron SET email = %s WHERE patron_id = %s"
        cursor.execute(update_email_query, (new_email, patron_id))
        conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.error as err:
        return f"Database error: {err}"

    return redirect(url_for('dashboard'))

# Route to add new books to library collection
@app.route('/add_new_book', methods=['POST'])
@login_required
def add_book_to_collection():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    isbn = request.form.get('isbn')
    page_count = request.form.get('page_count')
    publisher = request.form.get('publisher')
    title = request.form.get('title')
    genre = request.form.get('genre')
    blurb = request.form.get('blurb')
    pub_date = request.form.get('publish_date')

    conn = mysql.connector.connect(**_db_config())
    cursor = conn.cursor(dictionary=True)
    author_query = "SELECT * FROM Author WHERE first_name = %s AND last_name = %s LIMIT 1"
    cursor.execute(author_query, (first_name, last_name))
    author = cursor.fetchone()
    if author:
        author_id = author['author_id']
    else:
        insert_author_query = "INSERT INTO Author (first_name, last_name) VALUES (%s, %s)"
        cursor.execute(insert_author_query, (first_name, last_name))
        conn.commit()
        author_id = cursor.lastrowid
    cursor.close()
    conn.close()

    conn = mysql.connector.connect(**_db_config())
    cursor = conn.cursor(dictionary=True)
    book_query = "SELECT * FROM Book WHERE isbn = %s"
    cursor.execute(book_query, (isbn,))
    book = cursor.fetchone()
    if not book:
        book_insert_query = "INSERT INTO Book (isbn, author_id, page_count, publisher) VALUES (%s, %s, %s, %s)"
        values = (isbn, author_id, page_count, publisher)
        cursor.execute(book_insert_query, values)
        conn.commit()
    cursor.close()
    conn.close()

    conn = mysql.connector.connect(**_db_config())
    cursor = conn.cursor(dictionary=True)
    add_material_query = "INSERT INTO Material (title, blurb, material_type, genre, publish_date, availability) VALUES (%s, %s, %s, %s, %s, %s)"
    material_values = (title, blurb, 'book', genre, pub_date, 'available')
    try:
        cursor.execute(add_material_query, material_values)
        conn.commit()
    except mysql.connector.Error as err:
        conn.rollback()
        return f"Database error: {err}"
    cursor.close()
    conn.close()
    return redirect(url_for('dashboard'))

# Route to add new films to library collection
@app.route('/add_new_film', methods=['POST'])
@login_required
def add_film_to_collection():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    imdb_id = request.form.get('imdb_id')
    film_length = request.form.get('film_length')
    studio = request.form.get('studio')
    rating = request.form.get('rating')
    film_format = request.form.get('film_format')
    title = request.form.get('title')
    genre = request.form.get('genre')
    blurb = request.form.get('blurb')
    pub_date = request.form.get('publish_date')

    conn = mysql.connector.connect(**_db_config())
    cursor = conn.cursor(dictionary=True)
    director_query = "SELECT * FROM Director WHERE first_name = %s AND last_name = %s LIMIT 1"
    cursor.execute(director_query, (first_name, last_name))
    director = cursor.fetchone()
    if director:
        director_id = director['director_id']
    else:
        insert_director_query = "INSERT INTO Director (first_name, last_name) VALUES (%s, %s)"
        cursor.execute(insert_director_query, (first_name, last_name))
        conn.commit()
        director_id = cursor.lastrowid
    cursor.close()
    conn.close()

    conn = mysql.connector.connect(**_db_config())
    cursor = conn.cursor(dictionary=True)
    film_query = "SELECT * FROM Film WHERE imdb_id = %s"
    cursor.execute(film_query, (imdb_id,))
    film = cursor.fetchone()
    if not film:
        film_insert_query = "INSERT INTO Film (imdb_id, director_id, film_length, studio, rating, film_format) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (imdb_id, director_id, film_length, studio, rating, film_format)
        cursor.execute(film_insert_query, values)
        conn.commit()
    cursor.close()
    conn.close()

    conn = mysql.connector.connect(**_db_config())
    cursor = conn.cursor(dictionary=True)
    add_material_query = "INSERT INTO Material (title, blurb, material_type, genre, publish_date, availability) VALUES (%s, %s, %s, %s, %s, %s)"
    material_values = (title, blurb, 'film', genre, pub_date, 'available')
    try:
        cursor.execute(add_material_query, material_values)
        conn.commit()
    except mysql.connector.Error as err:
        conn.rollback()
        return f"Database error: {err}"
    cursor.close()
    conn.close()
    return redirect(url_for('dashboard'))

    

# Logout route that will clear the session and redirect to the login page
@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/apply_late_fees", methods=["POST"])
@login_required
def apply_late_fees():
    # Only staff or admin should apply late fees
    if session.get("role") not in ["staff", "admin"]:
        return redirect(url_for("dashboard"))

    try:
        conn = mysql.connector.connect(**_db_config())
        cursor = conn.cursor()

        cursor.callproc("apply_late_fees")
        conn.commit()

        cursor.close()
        conn.close()

        flash("Late fees applied successfully.", "success")

    except mysql.connector.Error as err:
        flash(f"Error applying late fees: {err}", "error")

    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    app.run(host="0.0.0.0", port=port, debug=True)

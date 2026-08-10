# Library Web App

Simple Flask website for your database systems class project.

## Features

- Login with three roles: patron, staff
- Role-based access pages
- Database connectivity check to your library schema

## Demo Login Credentials

- patron: `patron1` / `patron1`, `patron2` / `patron2`, `patron3` / `patron3`
- staff: `staff1` / `staff1`, `staff2` / `staff2`, `staff3` / `staff3`

## Run

1. Open SQL Workbench and run the library_ddl and library_dml files

2. Create and activate a vitual environment:

To create:

```bash
   python3 -m venv .venv
```

To activate:

```bash
   source .venv/bin/activate
```

3. Install dependencies:

   ```bash
      python3 -m pip install -r requirements.txt
   ```

4. Create .env file and set environment variables (use `.env.example` as a guide).

5. Start app:

   ```bash
   python3 app.py
   ```

6. Open [http://localhost:8000/login](http://localhost:8000/login)

## How We Met the Deliverable 5 Requirements

Important Note

1. The buttons with a lavender background color represent the functionality that we are using to meet the deliverable 5 requirements.

2. The buttons with a blue background color represent additional functionality we added beyond what is required for deliverable 5

When Logging in as a Patron...

1. First Query: The "View Library Fees" button shows the patron's unpaid fee total using a join and an aggregate function

2. Second Query: The "View Your Room Reservations" shows the patron's upcoming reservations using a view called Patron_Reservation_View

3. A Function: The "View Library Fees" button calculates the patron's total unpaid fees using a function

4. Operation Showcasing a Trigger: A trigger is in place to automatically deny any new reservation that takes place in the same room at the same day and time as an existing reservation. To view this, the patron can attempt to create a duplicate reservation using the "Add New Reservation" button and will see that it results in an error.

5. CRUD Functionality: The patron role is able to CREATE new reservations, READ mutliple tables of data, UPDATE their email address, and DELETE reservations they have created.

When Logging in as Staff

1. Third Query: The "View Patrons with Current Checkouts" button uses both a join and a subquery

2. Fourth Query: The "Search Library Book Collection" button uses a join

3. Fifth Query: The "View Total Checked Out Materials" button uses an aggregate function and a join in the query

4. A Procedure:The "Apply Late Fees" button uses a procedure to apply the late fees
   CRUD Functionality: The staff role is able to CREATE new patron accounts, READ mutliple tables of data, UPDATE late fee amounts, and DELETE patron accounts.

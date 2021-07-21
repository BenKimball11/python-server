import sqlite3
import json

from models import Employee

EMPLOYEES = [
    {
        "name": "atokad",
        "locationId": 1,
        "id": 1
    },
    {
        "name": "ben",
        "locationId": 2,
        "id": 2
    }
]

def get_all_employees():
    """Return a list of employees"""
    # Open a connection to the database
    with sqlite3.connect("./kennel.db") as conn:
        # Black box
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            e.id,
            e.name,
            e.address,
            e.location_id
        FROM employee e
        """)

        # Initialize an empty list to hold all employee representations
        employees = []
        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()
        # Iterate list of data returned from database
        for row in dataset:
            # Create an employee instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Employee class imported above.
            employee = Employee(row['id'], row['name'], row['address'],
                                row['location_id'])
            employees.append(employee.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(employees)



# SQL GET function
def get_single_employee(id):
    """Return a single employee by Id"""
    with sqlite3.connect("./kennel.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement
        db_cursor.execute("""
        SELECT
            e.id,
            e.name,
            e.address,
            e.location_id
        FROM employee e
        WHERE e.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()
        # Create an employee instance from the current row
        employee = Employee(data['id'], data['name'], data['address'],
                                data['location_id'])

        return json.dumps(employee.__dict__)



# SQL GET with query parameters
def get_employees_by_location(location_id):
    """Returns a list of locations by Id"""
    with sqlite3.connect("./kennel.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the info you want
        db_cursor.execute("""
        SELECT
            e.id,
            e.name,
            e.address,
            e.location_id
        FROM employee e
        WHERE e.location_id = ?
        """, ( location_id, ))

        employees = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            employee = Employee(row['id'], row['name'], row['address'],
                                row['location_id'])
            employees.append(employee.__dict__)

    return json.dumps(employees)


def create_employee(employee):
    """Create a NEW employee
    """
    # Get the id value of the last location in the list
    max_id = EMPLOYEES[-1]["id"]
    # Add 1 to whatever that number is
    new_id = max_id + 1
    # Add an `id` property to the employee dictionary
    employee["id"] = new_id
    # Add the employee dictionary to the list
    EMPLOYEES.append(employee)
    # Return the dictionary with `id` property added
    return employee


# SQL DELETE function
def delete_employee(id):
    """Delete an employee by Id"""
    with sqlite3.connect("./kennel.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM employee
        WHERE id = ?
        """, ( id, ))



def update_employee(id, new_employee):
    """Edit an employee by Id
    """
    # Iterate the EMPLOYEES list, but with enumerate() so that
    # you can access the index value of each item
    for index, employee in enumerate(EMPLOYEES):
        if employee["id"] == id:
            # Found the employee. Update the value.
            EMPLOYEES[index] = new_employee
            break
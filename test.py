import sqlite3

db_file = "data/product_tgdd.db"
db_conn = sqlite3.connect(db_file)

def list_tables() -> list[str]:
    """Retrieve the names of all tables in the database."""
    # Include print logging statements so you can see when functions are being called.
    print(' - DB CALL: list_tables')

    cursor = db_conn.cursor()

    # Fetch the table names.
    cursor.execute("SELECT * FROM laptops;")

    tables = cursor.fetchall()
    return [t[0] for t in tables]


list_tables()
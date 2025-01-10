import psycopg2

def list_tables() -> list[str]:
    """Retrieve the names of all tables in the public schema of the PostgreSQL database."""
    tables = []
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        sql = '''
        SELECT table_name FROM information_schema.tables WHERE table_schema='public';
        '''

        # Execute the query to list table names
        cursor.execute(sql)

        # Fetch all table names
        tables = [table[0] for table in cursor.fetchall()]

        # Close the cursor and connection
        cursor.close()
        conn.close()

    except psycopg2.Error as e:
        # Log the error or handle it as needed
        tables = []  # Return an empty list in case of an error

    return tables

if __name__ == '__main__':
    table_names = list_tables()
    print(table_names)
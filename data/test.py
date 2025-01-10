import psycopg2

def test_connection():
    """Test connection to the PostgreSQL database and execute a test query."""
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        print("✅ Connected to PostgreSQL database")

        # Create a cursor object
        cursor = conn.cursor()

        # Execute a test query
        cursor.execute("SELECT * FROM laptops WHERE rating IS NOT NULL ORDER BY rating DESC LIMIT 5;")

        # Fetch and print all rows from the result of the query
        rows = cursor.fetchall()
        for row in rows:
            print(row)

        # Close the cursor and connection
        cursor.close()
        conn.close()
        print("🔒 Connection closed.")
    except psycopg2.Error as e:
        print(f"❌ Error connecting to database: {e}")

if __name__ == '__main__':
    test_connection()
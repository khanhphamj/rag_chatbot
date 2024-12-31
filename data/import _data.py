import psycopg2
import pandas as pd
from sqlalchemy import create_engine

def create_connection():
    """Create a database connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        print("✅ Connected to PostgreSQL database")
        return conn
    except psycopg2.Error as e:
        print(f"❌ Error connecting to database: {e}")
        return None

def create_table(conn):
    """Create the laptops table in the PostgreSQL database."""
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS laptops (
        id SERIAL PRIMARY KEY,
        name TEXT,
        price TEXT,
        ram INTEGER,
        rom_type TEXT,
        rom INTEGER,
        screen_size REAL,
        screen_detail TEXT,
        cpu TEXT,
        gpu TEXT,
        battery TEXT,
        weight REAL,
        rating REAL,
        links_href TEXT,
        brand TEXT,
        series TEXT,
        is_laptopai BOOLEAN,
        is_laptopgaming BOOLEAN
    );
    """
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
        conn.commit()
        print("✅ Table created successfully.")
    except psycopg2.Error as e:
        print(f"❌ Error creating table: {e}")
    finally:
        cursor.close()

def import_data(csv_file, conn):
    """Import data from CSV file into the laptops table."""
    try:
        # Read the CSV file
        df = pd.read_csv(csv_file)
        print("✅ CSV file read successfully.")

        # Create SQLAlchemy engine
        engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/postgres')

        # Insert data into the laptops table
        df.to_sql('laptops', engine, if_exists='append', index=False)
        print("✅ Data imported successfully.")
    except Exception as e:
        print(f"❌ Error importing data: {e}")

def main():
    conn = create_connection()
    if conn is not None:
        create_table(conn)
        import_data('laptop_all_clean.csv', conn)
        conn.close()
        print("🔒 Connection closed.")
    else:
        print("❌ Cannot create the database connection.")

if __name__ == '__main__':
    main()
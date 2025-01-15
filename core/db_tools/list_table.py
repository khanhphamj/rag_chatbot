import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def list_tables() -> list[str]:
    """Retrieve the names of all tables in the public schema of the PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        cursor = conn.cursor()
        query = ("SELECT table_name "
                 "FROM information_schema.tables "
                 "WHERE table_schema='public';")
        cursor.execute(query)
        tables = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        print('DB-tools: list_tables')
        return tables
    except Exception as e:
        print(f"Error listing tables: {e}")
        return []
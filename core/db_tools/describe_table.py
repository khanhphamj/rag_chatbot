import os
import psycopg2
from dotenv import load_dotenv
from typing import List, Tuple, Optional

load_dotenv()

def describe_table(table_name: str) -> Optional[List[Tuple[str, str]]]:
    """Retrieve schema of a table (column name and data type)."""
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        cursor = conn.cursor()
        query = """
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = %s;
        """
        cursor.execute(query, (table_name,))
        schema = cursor.fetchall()
        cursor.close()
        conn.close()
        print('DB-tools: describe_table')
        return schema if schema else None
    except Exception as e:
        print(f"Error describing table {table_name}: {e}")
        return None

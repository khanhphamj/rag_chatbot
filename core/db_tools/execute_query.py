import os
import psycopg2
from dotenv import load_dotenv
from typing import List, Dict, Optional, Any  # Add `Any` to the import

load_dotenv()

def execute_query(sql_query: str) -> Optional[List[Dict[str, Any]]]:
    """Execute a SQL SELECT query and return results as a list of dictionaries."""
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        cursor = conn.cursor()
        cursor.execute(sql_query)
        columns = [desc[0] for desc in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return results
    except Exception as e:
        print(f"Error executing query: {e}")
        return None

import os
import psycopg2
from dotenv import load_dotenv
from typing import List, Dict, Tuple, Optional

load_dotenv()

def query_sample(table_names: List[str]) -> Dict[str, Optional[List[Tuple]]]:
    """Fetch sample data (up to 5 rows) from the specified tables."""
    results = {}
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        cursor = conn.cursor()
        for table_name in table_names:
            try:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 5;")
                results[table_name] = cursor.fetchall() or None
            except Exception as e:
                results[table_name] = None
        cursor.close()
        conn.close()
        return results
    except Exception as e:
        print(f"Error querying sample data: {e}")
        return {}
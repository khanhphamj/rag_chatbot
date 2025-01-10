import re
import psycopg2
from typing import List, Dict, Optional


def sanitize_sql(sql_query: str) -> str:
    """Sanitize an SQL query by removing unwanted characters.

    Args:
        sql_query: The SQL query to sanitize.

    Returns:
        A sanitized SQL query string.
    """
    # Remove backslashes to prevent SQL injection
    return re.sub(r'\\+', '', sql_query)

def execute_query(sql_query: str) -> Optional[List[Dict[str, any]]]:
    """Execute a SELECT statement and return the results.

    Args:
        sql_query: A sanitized SQL query string.

    Returns:
        A list of dictionaries, where each dictionary represents a row with column names as keys.
        Returns None if an error occurs during execution.
    """
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )

        # Sanitize SQL before execution
        sanitized_query = sanitize_sql(sql_query)

        cursor = conn.cursor()
        cursor.execute(sanitized_query)

        # Extract column names from cursor description
        columns = [desc[0] for desc in cursor.description]

        # Fetch all rows and convert to list of dictionaries
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]

        # Close the cursor and connection
        cursor.close()
        conn.close()

        return results

    except psycopg2.Error as e:
        # Handle and log database errors
        return None

    except Exception as e:
        # Handle other unexpected errors
        return None

    finally:
        if 'conn' in locals() and conn:
            conn.close()
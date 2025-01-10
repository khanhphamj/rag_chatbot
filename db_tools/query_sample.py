import psycopg2
from typing import List, Dict, Tuple, Optional

def query_sample(table_names: List[str]) -> Dict[str, Optional[List[Tuple]]]:
    """Retrieve a sample of data from multiple tables in the PostgreSQL database.

    Args:
        table_names: A list of table names to query.

    Returns:
        A dictionary where keys are table names and values are lists of rows
        (each row is a tuple of column values), or None if no data is found.
    """
    results = {}
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )

        cursor = conn.cursor()

        for table_name in table_names:
            try:
                query = f"SELECT * FROM {table_name} LIMIT 5;"
                cursor.execute(query)

                sample = cursor.fetchall()
                results[table_name] = sample if sample else None
            except psycopg2.Error as e:
                # Handle table-specific query errors, such as missing tables
                results[table_name] = None

        # Close the cursor and connection
        cursor.close()
        conn.close()

    except psycopg2.Error as e:
        # Handle connection or general database errors
        return {}

    return results


if __name__ == '__main__':
    table_names = ["laptops"]  # Replace with your actual table names
    samples = query_sample(table_names)
    print(samples)

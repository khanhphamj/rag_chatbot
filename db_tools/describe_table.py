import psycopg2
from typing import List, Tuple, Optional

def describe_table(table_name: str) -> Optional[List[Tuple[str, str]]]:
    """Look up the table schema.

    Args:
        table_name: The name of the table to describe.

    Returns:
        A list of tuples, where each tuple represents a column with its name and data type.
        Returns None if the table does not exist or an error occurs.
    """
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        query = """
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = %s;
        """
        cursor.execute(query, (table_name,))

        schema = cursor.fetchall()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        if not schema:
            # Return None if the table schema is empty or table does not exist
            return None

        # Return the schema as a list of tuples
        return [(col[0], col[1]) for col in schema]

    except psycopg2.Error as e:
        # Log or handle the error as needed
        return None

if __name__ == '__main__':
    table_name = 'laptops'
    schema = describe_table(table_name)
    print(f"Schema for table '{table_name}': {schema}")
import os
import google.generativeai as genai
from google.api_core import retry
from core.db_tools.list_table import list_tables
from core.db_tools.describe_table import describe_table
from core.db_tools.query_sample import query_sample
from core.db_tools.execute_query import execute_query
from instruction import INSTRUCTION
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional

# Load environment variables
load_dotenv()

# Configure the Google API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Retry policy for API requests
retry_policy = {"retry": retry.Retry(predicate=retry.if_transient_error)}

# Database tools available for the assistant
db_tools = [list_tables, describe_table, query_sample]

# Initialize the generative model with tools and instructions
model = genai.GenerativeModel(
    "models/gemini-1.5-flash-latest",
    tools=db_tools,
    system_instruction=INSTRUCTION
)

# Start a chat session with automatic function calling enabled
chat_session = model.start_chat(enable_automatic_function_calling=True)


def generate_alternative_query(original_query: str, attempt: int) -> Optional[str]:
    """
    Generates an alternative SQL query based on the original query.

    Args:
        original_query (str): The original SQL query that returned empty.
        attempt (int): The current retry attempt number.

    Returns:
        Optional[str]: A new SQL query or None if generation fails.
    """
    try:
        prompt = (
            f"The following SQL query returned no results:\n\n{original_query}\n\n"
            f"Please provide an alternative SQL query that might return results. "
            f"Attempt number {attempt}."
        )
        response = chat_session.send_message(prompt, request_options=retry_policy)
        new_query = response.text.strip()
        print(f"Generated alternative query on attempt {attempt}: {new_query}")
        return new_query
    except Exception as e:
        print(f"Error generating alternative query: {e}")
        return None


def execute_query_with_alternatives(sql_query: str, max_attempts: int = 3) -> Optional[List[Dict[str, Any]]]:
    """
    Executes a SQL query and, if it returns empty, generates and executes alternative queries.

    Args:
        sql_query (str): The initial SQL query to execute.
        max_attempts (int): Maximum number of attempts to generate alternative queries.

    Returns:
        Optional[List[Dict[str, Any]]]: The query results or None if all attempts fail.
    """
    current_query = sql_query
    for attempt in range(1, max_attempts + 1):
        result = execute_query(current_query)
        if result:
            print(f"Query succeeded on attempt {attempt}.")
            return result
        else:
            print(f"Attempt {attempt} with query returned empty.")
            if attempt < max_attempts:
                # Generate a new query based on the original query
                new_query = generate_alternative_query(sql_query, attempt)
                if new_query:
                    current_query = new_query
                else:
                    print("Failed to generate a new query.")
                    break
            else:
                print("Maximum attempts reached. No results found.")
    return None


# Add the alternative execute_query function to db_tools
db_tools.append(execute_query_with_alternatives)

# Re-initialize the generative model with the updated tools
model = genai.GenerativeModel(
    "models/gemini-1.5-flash-latest",
    tools=db_tools,
    system_instruction=INSTRUCTION
)

# Restart the chat session to include the updated tools
chat_session = model.start_chat(enable_automatic_function_calling=True)


def handle_query(user_input: str) -> str:
    """
    Handles user queries by interacting with the chat model.

    Args:
        user_input (str): The user's query.

    Returns:
        str: The assistant's response text.
    """
    try:
        # Send the message to the chat session
        response = chat_session.send_message(user_input, request_options=retry_policy)

        # Extract the response text
        return response.text
    except Exception as e:
        return f"Lỗi: {e}"


if __name__ == "__main__":
    # Interactive REPL loop for testing
    print("Xin chào! Tôi là Xám, trợ lý ảo của Thế Giới Di Động, chuyên tư vấn về sản phẩm laptop. Tôi có thể giúp gì cho bạn hôm nay?")
    while True:
        user_input = input("Bạn: ")
        if user_input.lower() in ["thoát", "exit", "quit", "q"]:
            print("Tạm biệt! Hẹn gặp lại bạn nhé.")
            break
        response = handle_query(user_input)
        print(f"Xám: {response}\n")
import warnings
import logging
from core.chatbot.assistant import start_chat
from google.api_core import retry
from google.generativeai.types import generation_types

# Suppress all warnings
warnings.filterwarnings("ignore")

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def test_chatbot_interaction():
    try:
        chat = start_chat()
        retry_policy = {"retry": retry.Retry(predicate=retry.if_transient_error)}

        message = ("Bạn là ai")
        logging.debug(f"Sending message: {message}")

        resp = chat.send_message(
            message,
            request_options=retry_policy
        )
        if resp and hasattr(resp, 'text'):
            logging.debug(f"Received response: {resp.text}")
            print(resp.text)
        else:
            logging.debug("No response received from chatbot.")
            print("Không nhận được phản hồi từ chatbot. Vui lòng thử lại.")
    except generation_types.StopCandidateException as e:
        logging.error(f"StopCandidateException: {e.args[0]}")
        print(f"Error: {e.args[0]}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    test_chatbot_interaction()
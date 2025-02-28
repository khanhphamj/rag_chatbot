import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import random
import logging

# Configure logging
logging.basicConfig(
    filename="scraping.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Path to input and output Excel files
DATA_PATH = "../data/laptop_all.xlsx"
OUTPUT_PATH = "../data/laptop_with_descriptions.xlsx"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


def fetch_and_process_content(url):
    """
    Fetch and process the content from the given URL.
    """
    try:
        # Send a GET request
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the desired div
        description_div = soup.find("div", {"class": "description tab-content short", "id": "tab-2"})
        if description_div:
            # Extract plain text
            plain_text = description_div.get_text(separator="\n", strip=True)

            # Remove the "Xem thêm" text if it exists
            plain_text = plain_text.replace("Xem thêm", "").strip()

            # Format the text into a meaningful structure
            formatted_text = (
                plain_text.replace("\n•", "\n\n•")  # Add double line breaks for bullets
                          .replace("\n", " ")      # Combine lines into paragraphs
                          .replace("  ", " ")      # Remove double spaces
            )
            return formatted_text
        else:
            return "Description div not found"
    except Exception as e:
        raise RuntimeError(f"Error fetching content from {url}: {e}")


def get_description_from_links(file_path):
    """
    Reads an Excel file with columns `name` and `links_href`, scrapes descriptions from <div id="tab-2">
    on each URL, and returns a DataFrame with an additional `description` column.
    """
    # Read the Excel file
    df = pd.read_excel(file_path)

    if 'name' not in df.columns or 'links_href' not in df.columns:
        raise ValueError("The input file must have `name` and `links_href` columns.")

    names = df['name']
    links = df['links_href']
    descriptions = []

    for index, (name, link) in enumerate(zip(names, links)):
        try:
            logging.info(f"Processing product {index + 1}/{len(links)}: {name} ({link})")
            # Fetch and process the content
            description = fetch_and_process_content(link)
            descriptions.append(description)
            logging.info(f"Successfully processed product: {name}")
        except Exception as e:
            descriptions.append(f"Error: {e}")
            logging.error(f"Error processing product {name}: {e}")

        # Sleep for a random duration to avoid being blocked
        time.sleep(random.uniform(1, 3))

    # Add the descriptions back to the DataFrame
    df['description'] = descriptions
    return df


def save_to_excel(df, output_path):
    """
    Save the DataFrame to an Excel file.
    """
    try:
        df.to_excel(output_path, index=False)
        logging.info(f"Data successfully saved to {output_path}")
    except Exception as e:
        logging.error(f"Error saving to Excel: {e}")
        raise


if __name__ == "__main__":
    try:
        # Process the data
        df_with_descriptions = get_description_from_links(DATA_PATH)

        # Save the updated DataFrame to an output file
        save_to_excel(df_with_descriptions, OUTPUT_PATH)
        print(f"Descriptions successfully added and saved to {OUTPUT_PATH}")

    except Exception as e:
        logging.critical(f"Critical error during execution: {e}")
        print(f"An error occurred: {e}")
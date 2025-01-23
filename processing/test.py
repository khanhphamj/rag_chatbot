import requests
from bs4 import BeautifulSoup

# Test URL
url = "https://www.thegioididong.com/laptop/msi-prestige-13-ai-a2vmg-ultra-7-258v-040vn"

# User-Agent to mimic a browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Function to fetch and process plain text content
def fetch_and_process_content(url):
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
        return f"Error: {e}"

# Fetch and print processed content
processed_text = fetch_and_process_content(url)
print(processed_text)

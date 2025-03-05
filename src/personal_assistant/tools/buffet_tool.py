import requests
from bs4 import BeautifulSoup


def get_buffet_tool() -> str:
    """
    Retrieves buffet information from a designated website using BeautifulSoup.
    """
   
    # URL of the buffet information page
    url = 'https://ramadanbuffetprice.com/best-ramadan-buffet-in-faisalabad-2025/'

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an error for non-200 responses
    except Exception as e:
        return f"Error fetching buffet information: {e}"

    # Parse the HTML response using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    content = soup.get_text(separator="\n", strip=True)
    return content
    # # Locate the content section containing buffet details.
    # # (You may need to adjust the selector based on the website's structure.)
    # content_div = soup.find('div', class_="site-content")
    
    # if content_div:
    #     # Extract and clean up the text from the content
    #     info_text = content_div.get_text(separator="\n", strip=True)
    #     # Optionally, you can limit the length of the returned text.
    #     return info_text if info_text else "Buffet information is currently unavailable."
    # else:
    #     return "Buffet information not found on the page."

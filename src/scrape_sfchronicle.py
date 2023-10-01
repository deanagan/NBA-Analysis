import requests
from bs4 import BeautifulSoup

url = 'https://www.sfchronicle.com/sports/warriors/article/warriors-offseason-schedule-key-dates-events-18114955.php'

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the specific element(s) you want to scrape
    # Modify the code below to match the structure of the target webpage
    target_elements = soup.find_all('p')

    # Extract the text content from the target elements
    scraped_content = [element.get_text(strip=True) for element in target_elements]

    # Print the scraped content
    for content in scraped_content:
        print(content)
else:
    print('Failed to retrieve the webpage. Status Code:', response.status_code)

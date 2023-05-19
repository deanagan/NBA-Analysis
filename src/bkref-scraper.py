import requests
from bs4 import BeautifulSoup

# Send a GET request to the webpage
url = 'https://www.basketball-reference.com/leagues/NBA_2023_games.html'
response = requests.get(url)

# Create a BeautifulSoup object from the response content
soup = BeautifulSoup(response.content, 'html.parser')

# Find the table containing the schedule
table = soup.find('table', id='schedule')

# Extract the schedule data from the table
schedule_data = []

for row in table.find_all('tr'):

    cells = row.find_all('td')

    if len(cells) >= 5:
        ad = row.find_all('a')
        print(ad[0].text)
        print('td cells')
        date = cells[0].text
        print(cells[0])
        print(cells[1].text)
        print(cells[3].text)
        print(cells[5].text)
        print(cells[6].text)
        print(cells[7].text)
        print(cells[8].text)
        print(cells[9].text)
        visitor_team = cells[2].text
        home_team = cells[4].text
        schedule_data.append((date, visitor_team, home_team))
        break


# Print the schedule data
for game in schedule_data:
    print(game)
    break
    print(f"Date: {game[0]}, Visitor: {game[1]}, Home: {game[2]}")

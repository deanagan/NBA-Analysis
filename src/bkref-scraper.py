from enum import unique
import sched
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import calendar
import pandas as pd
import time


def parse_month(url):
    time.sleep(5)  # Adding a sleep, otherwise, we get 429 error
    # Create a BeautifulSoup object from the response content
    response = requests.get(url)
    if response.status_code == 429:
        retry_after = response.headers.get('Retry-After')
        print("You received a 429 status code. Retry after:", retry_after)
    else:
        print("Request was successful.")

    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table containing the schedule
    table = soup.find('table', id='schedule')

    # Extract the schedule data from the table
    for row in table.find_all('tr'):
        try:
            cells = row.find_all('td')
            if len(cells) >= 5:
                ad = row.find_all('a')
                date = f'{ad[0].text} {cells[0].text}'
                visitor_team = cells[1].text
                visitor_score = cells[2].text
                home_team = cells[3].text
                home_score = cells[4].text
                datetimeobj = datetime.strptime(
                    f'{date}m', "%a, %b %d, %Y %I:%M%p")

                end_of_regular_season = datetime(2023, 4, 10)
                # print(date, visitor_team, visitor_score, home_team, home_score)
                if datetimeobj >= end_of_regular_season:
                    continue

                yield (date, datetimeobj, visitor_team, int(visitor_score), home_team, int(home_score))
        except ValueError as e:
            # Exception handling
            print("Caught an exception:", e)


def get_url(year, month):
    return f'https://www.basketball-reference.com/leagues/NBA_{year}_games-{month}.html'


unique_teams = {'Orlando Magic', 'Boston Celtics', 'Philadelphia 76ers', 'Atlanta Hawks', 'Washington Wizards', 'New York Knicks', 'Minnesota Timberwolves', 'San Antonio Spurs', 'Brooklyn Nets', 'Houston Rockets', 'Golden State Warriors', 'Miami Heat', 'Indiana Pacers', 'New Orleans Pelicans', 'Oklahoma City Thunder',
                'Denver Nuggets', 'Los Angeles Clippers', 'Los Angeles Lakers', 'Dallas Mavericks', 'Chicago Bulls', 'Toronto Raptors', 'Memphis Grizzlies', 'Detroit Pistons', 'Portland Trail Blazers', 'Sacramento Kings', 'Cleveland Cavaliers', 'Phoenix Suns', 'Milwaukee Bucks', 'Utah Jazz', 'Charlotte Hornets'}


def get_team_schedule_analysis(year, team):
    # Get a list of month names
    month_strings = list(calendar.month_name)

    # Remove the empty first element
    month_strings = [month.lower() for month in month_strings[1:]]
    season_months = month_strings[9:] + month_strings[:4]

    record = (0, 0)
    b2b_games = 0
    road_b2b_games = 0

    for month in season_months:
        url = get_url(year, month)
        prev_data = None
        for date, datetimeobj, visitor, vscore, home, hscore in parse_month(url):

            w, l = record
            if visitor == team:
                if vscore > hscore:
                    record = (w + 1, l)
                else:
                    record = (w, l + 1)

                if prev_data != None and (datetimeobj - prev_data[1]) < timedelta(hours=40):
                    b2b_games += 1

                    if prev_data[2] == team:
                        road_b2b_games += 1
                prev_data = date, datetimeobj, visitor, vscore, home, hscore
            elif home == team:
                if hscore > vscore:
                    record = (w + 1, l)

                else:
                    record = (w, l + 1)

                if prev_data != None and (datetimeobj - prev_data[1]) < timedelta(hours=40):
                    b2b_games += 1

                prev_data = (date, datetimeobj, visitor, vscore, home, hscore)

    return record, b2b_games, road_b2b_games


def add_data_frame(data):
    data = (('John', 25, 'USA'), ('Emily', 30, 'Canada'), ('Michael', 35, 'UK'))

    df = pd.DataFrame(data, columns=[
                      'Team', 'Record', 'Back-To-Back Games', 'Road Back-To-Back Games'])

    return df


if __name__ == "__main__":
    year = 2023  # Applies to 2022-2023 season
    team = 'Golden State Warriors'

    record, b2b_games, road_b2b_games = get_team_schedule_analysis(
        year, team)

    print(f'{team} Record {record}, Back-To-Back Games {b2b_games}, Road Back-To-Back Games {road_b2b_games}')

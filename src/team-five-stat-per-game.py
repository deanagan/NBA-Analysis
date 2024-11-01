# This script does

# 1. Scrape the page
# 2. Parse the outcome
# 3. Determine stats for the 5 in a game
from bs4 import BeautifulSoup
import requests
import re


from bs4 import BeautifulSoup
import requests

website = requests.get(
    'https://www.nba.com/game/gsw-vs-lac-0022200871/play-by-play?watchFullGame=&period=Q1')
print(website)

soup = BeautifulSoup(website.content, 'html.parser')


# h2tags = soup.find_all('h2')

# for soups in h2tags:
#     print(soups.string)

# play_by_play_divs = soup.find_all(
#     'span', {'class': re.compile('^GamePlayByPlay')})
spans = soup.find_all('span')  # , {'scoring_is_false': True})

# iterate over the results and do something with each div
for span in spans:
    print(span)


# <tr class = "playByPlay__tableRow Table__TR Table__TR--sm Table__even" data-idx = "0" >
#   <td class = "playByPlay__time Table__TD" > 12: 00 < /td >
#    <td class = "playByPlay__logo Table__TD" >
#       <img alt = "" class = "Image Logo Logo__sm" data-mptype = "image" src = "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"/>
#     </td >
#     <td class = "playByPlay__text tl Table__TD" colspan = "1" > Kevon Looney vs. Ivica Zubac(Marcus Morris Sr. gains possession) < /td >
#     <td class = "playByPlay__score playByPlay__score--away tr Table__TD" > 0 < /td >
#     <td class = "playByPlay__score playByPlay__score--home tr Table__TD" > 0 < /td >
# </tr >

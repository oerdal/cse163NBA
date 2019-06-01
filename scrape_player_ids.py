# purpose of this module is to use
# python technologies to scrape player
# id numbers from stats.nba.com for later use

import requests
import os
from bs4 import BeautifulSoup
import re
import json
import scraper_utils

base_url_1 = 'https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=PerGame&Scope=S&Season='
base_url_2 = '&SeasonType=Regular+Season&StatCategory=PTS'
headers = requests.utils.default_headers()
headers.update({
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
})

def get_k_leaders_for_year(year, k):
    leaders = {}
    req = requests.get(base_url_1 + year + base_url_2, headers=headers)
    player_data = req.json()
    players = player_data['resultSet']['rowSet']

    for player in players[:k]:
        player_id, name = player[0], player[2]
        name = re.sub(' ', '_', name)
        leaders[name] = player_id

    return leaders


def get_k_leaders_in_range(start_year, end_year, k):
    data = {}

    for i in range(start_year, end_year + 1):
        year = scraper_utils.format_year(i)
        print('---------- STARTING ' + year + ' ----------')
        data[year] = get_k_leaders_for_year(year, k)
        print(data[year])

    return data

with open('data/top_10_ids.json', 'w') as file:
    data = get_k_leaders_in_range(1994, 2019, 10)
    file.write(json.dumps(data))
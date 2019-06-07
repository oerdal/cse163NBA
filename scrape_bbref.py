# purpose of this module is to use
# python technologies to scrape player
# data from bbref, and eventually store it

import requests
import os
from bs4 import BeautifulSoup
import pandas as pd

base_url1 = 'https://www.basketball-reference.com/leagues/NBA_'
base_url2 = '_per_game.html'

# concatenate the two above strings, with a given year in between,
# to get all player stats for that year, e.g. 2000 gives 1999-2000 stats
# 2019 gives 2018-19 etc.
def get_headers():
    req = requests.get(base_url1 + '2019' + base_url2)
    playerSoup = BeautifulSoup(req.text, "html.parser")
    stat_head = playerSoup.select('table > thead')
    table_head = BeautifulSoup(str(stat_head), 'html.parser')
    headers = []
    for h in table_head.select('th'):
        headers.append(h.getText())
    headers.append('Year')
    return headers

def scrape_stats(headers):
    all_player_data = []
    for i in range(2000,2020):
        req = requests.get(base_url1 + str(i) + base_url2)
        playerSoup = BeautifulSoup(req.text, "html.parser")
        # get stats for each provided stat in the features param
        stat_body = playerSoup.select('table > tbody')
        # parse the table head section to get headers
        # parse the table body section to get player data
        table_body = BeautifulSoup(str(stat_body), 'html.parser')
        players = table_body.select('tr')
        for j, player in enumerate(players):
            curr_player_data = []
            curr_player_data.append(j)
            player_data = BeautifulSoup(str(player), 'html.parser')
            player_stats = player_data.select('td')
            for stat in player_stats:
                if len(stat.getText()) > 0:
                    curr_player_data.append(stat.getText().replace('*', ''))
                else:
                    curr_player_data.append('-')
            curr_player_data.append(int(i))
            all_player_data.append(curr_player_data)
    data = pd.DataFrame(all_player_data, columns=headers)
    data.to_csv('data/player_data.csv')

    return None

headers = get_headers()
scrape_stats(headers)
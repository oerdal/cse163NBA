# purpose of this module is to use
# python technologies to scrape player
# id numbers from stats.nba.com for later use

import requests
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import re
import json

base_url_1 = 'https://stats.nba.com/leaders/?Season='
base_url_2 = '&SeasonType=Regular%20Season'

options = webdriver.FirefoxOptions()
options.add_argument('-headless')
capa = DesiredCapabilities.FIREFOX
capa["pageLoadStrategy"] = "none"

def get_leaders_for_year(year):
    leaders = {}
    url = base_url_1 + year + base_url_2
    driver = webdriver.Firefox(firefox_options=options, desired_capabilities=capa)
    driver.set_window_size(1440,900)
    driver.get(url)
    time.sleep(15)

    req_text = driver.page_source
    leader_soup = BeautifulSoup(req_text, 'html.parser')
    stat_body = leader_soup.select('.nba-stat-table tbody')
    table_body = BeautifulSoup(str(stat_body), 'html.parser')
    players = table_body.select('td.player > a')[:10]

    for player in players:
        name = re.sub(' ', '_', re.sub('[><]', '', re.search('>.*<', str(player)).group(0)))
        player_id = re.sub('[^0-9]', '', re.search('player/[0-9]*/traditional', str(player)).group(0))
        leaders[name] = player_id

    return leaders

leaders = get_leaders_for_year('2018-19')
print(leaders)
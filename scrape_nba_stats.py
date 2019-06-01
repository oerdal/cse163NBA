import requests, time, json
import pandas as pd
import numpy as np
import scraper_utils

# goal, scrape player shooting data for set of specific NBA players, use this
# data to power shot chart visualizations

# specific players: want to emphasize the uniqueness of the play style of the
# warriors, need data for key players -> Klay Thompson, Stephen Curry, Kevin Durant

# want to be able to make comparison of Warriors now to past juggernauts
# e.g. Lebron-era Heat, Late 2000s Spurs, early 2000s Lakers

# to do: get data for Lebron James + Dwyane Wade + Chris Bosh for Heat
#            data for Tony Parker, Manu Ginobilli, Tim Duncan for Spurs
#            data for 

# general plots -> 3 pointers per season from 1990-2019
#               -> 

stat_url_1 = 'https://stats.nba.com/stats/shotchartdetail?AheadBehind=&CFID=33&ClutchTime=&Conference=&ContextFilter=&ContextMeasure=FGA&DateFrom=&DateTo=&Division=&EndPeriod=10&EndRange=28800&GROUP_ID=&GameEventID=&GameID=&GameSegment=&GroupID=&GroupMode=&GroupQuantity=5&LastNGames=0&LeagueID=00&Location=&Month=0&OnOff=&OpponentTeamID=0&Outcome=&PORound=0&Period=0&PlayerID1=&PlayerID2=&PlayerID3=&PlayerID4=&PlayerID5=&PlayerPosition=&PointDiff=&Position=&RangeType=0&RookieYear=&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StartPeriod=1&StartRange=0&StarterBench=&TeamID=0&VsConference=&VsDivision=&VsPlayerID1=&VsPlayerID2=&VsPlayerID3=&VsPlayerID4=&VsPlayerID5=&VsTeamID=&CFPARAMS='
stat_url_2 = '&Season='
stat_url_3 = '&PlayerID='
LEADERS = np.load('data/top_10_ids.npy', allow_pickle=True).item()
PLAYERS = {'Stephen_Curry': 201939, 'Klay_Thompson': 202691, 'Kevin_Durant': 201142}
YEARS = {'2014-15', '2015-16', '2016-17', '2017-18', '2018-19'}
headers = requests.utils.default_headers()
headers.update({
    "user-agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
})

# for each key (player) in the PLAYERS dictionary, go to the appropriate stat URL for
# this player, and save the stats to CSV

def get_all_player_data():
    data = []
    for k, v in PLAYERS.items():
        for y in YEARS:
            # iterate over years from 2014 to 2019, getting shot data
            # for each player
            url = stat_url_1 + str(y) + stat_url_2 + str(y) + stat_url_3 + str(v)
            # get JSON player data
            curr_season_player_data = requests.get(url, headers=headers).json()
            data.append(curr_season_player_data)
            print("Data for player {}, for season {} collected".format(k, y))
    return data


def get_leader_data_for_year(year):
    data = []
    fmt_year = scraper_utils.format_year(year)
    for p_name, p_id in PLAYERS[fmt_year]:
        url = stat_url_1 + fmt_year + stat_url_2 + fmt_year + stat_url_3 + str(p_id)
        curr_season_leader_data = requests.get(url, headers=headers).json()
        data.append(curr_season_leader_data)
        print('Data for player {}, for season {} collected'.format(p_name, fmt_year))
    return data
    


def convert_to_df(data):
    data_frames = []
    # the resultsSet list contains a dictionary in its first index,
    # the key headers in that dictionary points to the headers for
    # the data we want to access for each player
    headers = data[0]['resultSets'][0]['headers']
    # the resultsSet list also contains the data for the data frame in
    # the same dictionary
    for player_season in data:
        player_season_data = player_season['resultSets'][0]['rowSet']
        # convert JSON data to data frame
        player_season_df = pd.DataFrame.from_records(data=player_season_data, columns=headers)
        data_frames.append(player_season_df)
    
    return pd.concat(data_frames, ignore_index=True)

# data = get_all_player_data()
# df = convert_to_df(data)
# df.to_csv('shots/shot_data.csv')
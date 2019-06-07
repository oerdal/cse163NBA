# Aashray Anand and Ozan Erdal
# CSE 163 Final Project: Observing trends in NBA shot selection, and 
# deriving a relationship between shot selection and performance

# this file contains all of the code needed to output the content that makes
# this report, it utilzes the data found in the shots/ and data/ folders to
# make every visualization, or prediction, the data visualizations are stored
# in different folders based on the types of content. e.g. the shot charts
# are stored in the shot_charts directory, the barplot and scatterplots are
# stored in the plots directory

# the python scrapers that were written to collect all of the data needed for
# this project are:
# scrape_player_ids.py
# scrape_nba_stats.py
# scrape_bbref.py
# scraper_utils.py (utilities only)

# to get all of the data again, the files can be run in the above order, excluding
# scraper_utils.py

# after the above files are run (this is unnecessary since we are submitting the assignment
# with the data, but can be done anyways to check for correctness), the current file can be
# run to generate all the data visualizations, and output the results of our predictions
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from plot_utils import make_shot_chart

# highest scoring player per year, used to generate plots for each
# of the years top scorers
max_player_per_year = {
    1999: 'Shaquille O\'Neal',
    2000: 'Allen Iverson',
    2001: 'Allen Iverson',
    2002: 'Tracy McGrady',
    2003: 'Tracy McGrady',
    2004: 'Allen Iverson',
    2005: 'Kobe Bryant',
    2006: 'Kobe Bryant',
    2007: 'LeBron James',
    2008: 'Dwyane Wade',
    2009: 'Kevin Durant',
    2010: 'Kevin Durant',
    2011: 'Kevin Durant',
    2012: 'Carmelo Anthony',
    2013: 'Kevin Durant',
    2014: 'Russell Westbrook',
    2015: 'Stephen Curry',
    2016: 'Russell Westbrook',
    2017: 'James Harden',
    2018: 'James Harden',
}

# creates a usable YEAR field
def clean_shots(shots):
    shots['YEAR'] = shots['GAME_DATE'].astype(str)
    for i, _ in shots.iterrows():
        res = shots.at[i, 'YEAR']
        shots.at[i, 'YEAR'] = res[0:4]
    shots['YEAR'] = shots['YEAR'].astype(int)
    return shots


# plots the number of two and three point shots taken by the league
# leaders for the years 1999-2019
def plot_twos_and_threes(all_year_shots):
    fig, [ax1, ax2] = plt.subplots(2, figsize=(16, 16))
    twos_per_year = all_year_shots.groupby('YEAR')['two'].sum()
    threes_per_year = all_year_shots.groupby('YEAR')['three'].sum()
    two_clrs = ['grey' if (x < max(twos_per_year)) else 'red' for x in twos_per_year]


# plots the number of two and three point shots averages per team per
# game for the years 1999-2019
def plot_twos_and_threes_teams(league_data):
    fig, [ax1, ax2] = plt.subplots(2, figsize=(13,13))
    ax1.title.set_text("average 2 pointers per game (per team)")
    league_twos = league_data.groupby('Year')['2PA'].mean()
    clrs = ['grey' if (x < max(league_twos) and x > min(league_twos)) else 'blue' if (x == min(league_twos)) else 'red' for x in league_twos]
    sns.barplot(x=league_twos.index, y=league_twos.values, palette=clrs, ax=ax1)

    ax2.title.set_text("average 3 pointers per game (per team)")
    league_threes = league_data.groupby('Year')['3PA'].mean()
    clrs = ['grey' if (x < max(league_threes) and x > min(league_threes)) else 'blue' if (x == min(league_threes)) else 'red' for x in league_threes]
    sns.barplot(x=league_threes.index, y=league_threes.values, palette=clrs, ax=ax2)
    plt.savefig('./plots/twos_and_threes_teams.png')


def main():
    # league statistical averages per team per game for 1999-2019
    league_data = pd.read_csv('./data/league_averages.csv')
    # compute 2 pointers attempted column, by subtracting the 3 pointers
    # attempted for each row from the total field goals attempted
    league_data['2PA'] = league_data['FGA'] - league_data['3PA']
    # create usable Year column
    for i, _ in league_data.iterrows():
        res = league_data.at[i, 'Year'].split('-')
        league_data.at[i, 'Year'] = '20' + res[1]
    shots_19 = pd.read_csv('./shots/current_year_shot_data.csv')
    # shot chart data for top 5 scoring players every year 2000-2019
    all_year_shots = pd.read_csv('shots/all_year_shot_data.csv')
    shots_19 = clean_shots(shots_19)
    all_year_shots = clean_shots(all_year_shots)
    # for the leading scorer in each season, generate a shot chart
    # and save it to the shot_charts directory
    for k, v in max_player_per_year.items():
        make_shot_chart(all_year_shots, name=v, year=k)
    # add numerical feature to shot chart data sets for type of shots
    all_year_shots['two'] = all_year_shots.SHOT_TYPE == '2PT Field Goal'
    all_year_shots['three'] = all_year_shots.SHOT_TYPE == '3PT Field Goal'
    shots_19['two'] = shots_19.SHOT_TYPE == '2PT Field Goal'
    shots_19['three'] = shots_19.SHOT_TYPE == '3PT Field Goal'
    # output a bar plot of the number of 2 point and 3 point field goals
    # per year, this chart is saved as twos_and_threes.png in plots/
    plot_twos_and_threes(all_year_shots)
    plot_twos_and_threes_teams(league_data)


if __name__ == '__main__':
    main()

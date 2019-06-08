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

# to get all of the data again, the files can be run in the above order,
#  excluding
# scraper_utils.py

# after the above files are run (this is unnecessary since we are submitting
# the assignment with the data, but can be done anyways to check
# for correctness), the current file can be run to generate all the data
# visualizations, and output the results of our predictions
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc
import seaborn as sns

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



# credit to http://savvastjortjoglou.com/nba-shot-sharts.html for
# the below utility function, which draws a basketball court using
# patches in matplotlib
# we can draw a set of matplotlib shapes on the above plot, to be 
# able to build a more powerful data visualization
def make_court(ax=None, color='black', lw=2, outer_lines=False):
    if ax is None:
        ax = plt.gca()
    elem = []
    rim = Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False)
    elem.append(rim)
    corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw,
                               color=color)
    elem.append(corner_three_a)
    corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
    elem.append(corner_three_b)
    three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw,
                    color=color)
    elem.append(three_arc)
    backboard = Rectangle((-30, -7.5), 60, -1, linewidth=lw, color=color)

    # The paint
    # Create the outer box 0f the paint, width=16ft, height=19ft
    outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color,
                          fill=False)
    # Create the inner box of the paint, widt=12ft, height=19ft
    inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color,
                          fill=False)

    # Create free throw top arc
    top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180,
                         linewidth=lw, color=color, fill=False)
    # Create free throw bottom arc
    bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0,
                            linewidth=lw, color=color, linestyle='dashed')
    # Restricted Zone, it is an arc with 4ft radius from center of the hoop
    restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw,
                     color=color)
    center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0,
                           linewidth=lw, color=color)
    center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0,
                           linewidth=lw, color=color)
    back_bound = Rectangle((-250,-47.5), 500, 0, color=color, linewidth=lw)
    left_bound = Rectangle((-250,-47.5), 0, 470, color=color, linewidth=lw)
    right_bound = Rectangle((250,-47.5), 0, 470, color=color, linewidth=lw)
    center_court = Rectangle((-250, 422.5), 500, 0, color=color, linewidth=lw)
    elem.append(center_inner_arc)
    elem.append(center_outer_arc)
    elem.append(backboard)
    elem.append(outer_box)
    elem.append(inner_box)
    elem.append(top_free_throw)
    elem.append(bottom_free_throw)
    elem.append(restricted)
    elem.append(back_bound)
    elem.append(left_bound)
    elem.append(right_bound)
    elem.append(center_court)
    for e in elem:
        ax.add_patch(e)
    return ax


# additional utility function added to utilize above function, plots the
# shot data for a given player (optionally, but always supplied),
# and optionally a given year
def make_shot_chart(shots, name=None, ax=None, year=None):
    if name is not None:
        data = shots[(shots['PLAYER_NAME'] == name)]
    else:
        data = shots
    if year is not None:
        data = data[data['YEAR'] == year]
    plt.figure(num=None, figsize=(11, 11), dpi=80, facecolor='w', edgecolor='k')
    ax = plt.gca() if ax is None else ax
    make_court(ax=ax, outer_lines=True)
    sns.scatterplot(x="LOC_X", y="LOC_Y", data=data, hue='SHOT_MADE_FLAG', ax=ax)
    plt.xlim(-300, 300)
    plt.ylim(-100, 500)
    plt.xlabel("")
    plt.ylabel("")
    plt.title("Shot chart: {}".format(name))
    file = "./shot_charts/" + str(name) + "_" + str(year) + ".png"
    plt.savefig(file)
    plt.show()


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
    _, [ax1, ax2] = plt.subplots(2, figsize=(16, 16))
    twos_per_year = all_year_shots.groupby('YEAR')['two'].sum()
    threes_per_year = all_year_shots.groupby('YEAR')['three'].sum()
    two_clrs = ['grey' if (x < max(twos_per_year)) else
                'red' for x in twos_per_year]
    three_clrs = ['grey' if (x < max(threes_per_year)) else
                  'red' for x in threes_per_year]
    sns.barplot(x=twos_per_year.index, y=twos_per_year.values,
                ax=ax1, palette=two_clrs)
    ax1.title.set_text("2 point field goals per year (top 5 players)")
    sns.barplot(x=threes_per_year.index, y=threes_per_year.values, ax=ax2,
                palette=three_clrs)
    ax2.title.set_text("3 point field goals per year (top 5 players)")
    plt.savefig('./plots/twos_and_threes.png')


# plots the number of two and three point shots averages per team per
# game for the years 1999-2019
def plot_twos_and_threes_teams(league_data):
    _, [ax1, ax2] = plt.subplots(2, figsize=(13, 13))
    ax1.title.set_text("average 2 pointers per game (per team)")
    league_twos = league_data.groupby('Year')['2PA'].mean()
    clrs = ['grey' if (x < max(league_twos) and x > min(league_twos)) else
            'blue' if (x == min(league_twos)) else 'red' for x in league_twos]
    sns.barplot(x=league_twos.index, y=league_twos.values,
                palette=clrs, ax=ax1)

    ax2.title.set_text("average 3 pointers per game (per team)")
    league_threes = league_data.groupby('Year')['3PA'].mean()
    clrs = ['grey' if (x < max(league_threes) and x > min(league_threes)) else
            'blue' if (x == min(league_threes)) else 'red' for x in
            league_threes]
    sns.barplot(x=league_threes.index, y=league_threes.values, palette=clrs,
                ax=ax2)
    plt.savefig('./plots/twos_and_threes_teams.png')


def plot_percentages_from_spots(shot_data_only):
    agg_per_spot = shot_data_only.groupby('SHOT_ZONE_BASIC').sum()
    agg_per_spot["percentage"] = agg_per_spot['SHOT_MADE_FLAG'] / agg_per_spot[
                                              'SHOT_ATTEMPTED_FLAG']
    agg_per_spot
    _, ax = plt.subplots(1, figsize=(15, 15))
    ax.title.set_text("shooting percentage from different court areas")
    sns.barplot(x=agg_per_spot.index, y=agg_per_spot['percentage'], palette=[
                                                     'grey'], ax=ax)
    plt.savefig('./plots/percentages_from_spots.png')


def main():
    plt.style.use('fivethirtyeight')
    # league shot data
    # league statistical averages per team per game for 1999-2019
    league_data = pd.read_csv('./data/league_averages.csv')
    # compute 2 pointers attempted column, by subtracting the 3 pointers
    # attempted for each row from the total field goals attempted
    league_data['2PA'] = league_data['FGA'] - league_data['3PA']
    # make Year column
    league_data['Year'] = league_data['Season']
    # make usable Year column
    for i, _ in league_data.iterrows():
        res = league_data.at[i, 'Year'].split('-')
        league_data.at[i, 'Year'] = '20' + res[1]
    # shot data for top 250 scoring players in 2019, will be used
    # for training and testing a classifier f
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
    plot_percentages_from_spots(shots_19)


if __name__ == '__main__':
    main()

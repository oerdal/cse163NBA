from scraper_utils import assert_equals

import project_demo as demo
import scraper_utils

import pandas as pd

CURRENT_YEAR_DATA = './shots/current_year_shot_data.csv'
ALL_YEAR_DATA = './shots/all_year_shot_data.csv'

curr_data = pd.read_csv(CURRENT_YEAR_DATA)
all_data = pd.read_csv(ALL_YEAR_DATA)


def test_project_demo():
    print('Testing project demo')

    # Checks that each year is storing 250 players' information
    assert_equals(250, len(set(curr_data['PLAYER_NAME'])))

    # Checks that data was collected for 19 seasons (2000-2019)
    # and that the clean_shots function works
    print('Cleaning shots')
    cleaned_shots = demo.clean_shots(all_data)
    dates = all_data.sort_values(by='GAME_DATE')['GAME_DATE']

    assert_equals(19, dates[len(all_data) - 1]//10000 - dates[0]//10000)
    assert_equals(19, cleaned_shots.at[len(cleaned_shots) - 1, 'YEAR'] -
                  cleaned_shots.at[0, 'YEAR'])


def test_scraper_utils():
    print('Testing scraper utils')

    # Checks that year format works for y2k
    assert_equals('1999-00', scraper_utils.format_year(2000))

    # Checks that year format works for current year
    assert_equals('2018-19', scraper_utils.format_year(2019))


def main():
    test_project_demo()
    test_scraper_utils()


if __name__ == '__main__':
    main()
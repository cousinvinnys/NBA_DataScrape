from datetime import date, timedelta
from hashlib import new
from matplotlib.pyplot import get
from nba_api.stats.endpoints import boxscoretraditionalv2 as box_score
from nba_api.stats.endpoints import teamgamelog
from nba_api.stats.static import teams
from nba_api.stats.static import players


import pandas as pd
import numpy as np
nba_teams = teams.get_teams()


def get_team_id_abbrev(team_name):
    temp_team = [team for team in nba_teams if team['abbreviation'] == team_name][0]
    return temp_team['id']


def did_play_yesterday(teamID):

    teamGameLog = teamgamelog.TeamGameLog(team_id=teamID)
    gameListDF = teamGameLog.get_data_frames()[0].iloc[0]['GAME_DATE']
    formatted_date = pd.to_datetime(gameListDF)

    if(formatted_date == date.today() - timedelta(days=1)):
        print("yes, your team played yesterday!")
        return True
    else:
        print("no, your team did not play yesterday")
        return False


did_play_yesterday(get_team_id_abbrev('IND'))

cavsID = get_team_id_abbrev('MIA')
# print(cavsID)

# Cavs gamelog from this season
cavsGameLog = teamgamelog.TeamGameLog(team_id=cavsID)

# Get the latest game
cavsGameLog_latest = cavsGameLog.get_data_frames()
# print(cavsGameLog_latest)

# print(cavsGameLog_latest[0].iloc[0])

new_df = cavsGameLog_latest[0].iloc[0]
# print(new_df)

# print(new_df['GAME_DATE'])

# Save the game date
game_date = new_df['GAME_DATE']

# Compare the game date to the current date

# print(game_date)
# print(dt.datetime.now())
formatted_date = pd.to_datetime(game_date)
# print(formatted_date)

# Check if formatted_date is equal to yesterday's date
# if(formatted_date == date.today() - timedelta(days=1)):
#print("yes, your team played yesterday!")
# else:
#print("no, your team did not play yesterday")

yesterdays_date = date.today() - timedelta(1)


# creating the date object of today's date
todays_date = date.today()
#print("Today's Date: ", todays_date)

#print("Yesterday's date: ", yesterdays_date)

# Check if a game was played yesterday


# importing date class from datetime module


# printing todays date
#print("Current date: ", todays_date)

# fetching the current year, month and day of today
#print("Current year:", todays_date.year)
#print("Current month:", todays_date.month)
#print("Current day:", todays_date.day)


testBoxScore = box_score.BoxScoreTraditionalV2(game_id='0022100825')
df = testBoxScore.get_data_frames()[1]

# print(df)

"""
dropped_columns = ['COMMENT', 'MIN', 'NICKNAME', 'TEAM_CITY', 'START_POSITION']

for column in dropped_columns:
    df = df.drop([column], axis='columns')

dropped_rows = [12]

for row in dropped_rows:
    df = df.drop([row], axis='rows')


# df = df.astype({"PTS": 'int', ""})

cleaned_columns = ['PTS', 'PLUS_MINUS', 'PF', 'TO', 'BLK', 'STL', 'AST', 'REB', 'DREB', 'OREB', 'FTA', 'FTM', 'FG3A', 'FG3M', 'FGA', 'FGM']

for column in cleaned_columns:
    df[[column]] = df[[column]].apply(np.int64)


# print(df)
# print(df.columns)

"""

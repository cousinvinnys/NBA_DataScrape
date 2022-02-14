from datetime import date, timedelta, datetime
from hashlib import new
from matplotlib.pyplot import get
from nba_api.stats.endpoints import boxscoretraditionalv2 as box_score
from nba_api.stats.endpoints import teamgamelog
from nba_api.stats.static import teams
from nba_api.stats.static import players

import pandas as pd
import numpy as np

# Returns the ID of the team designated by the abbreviation
def get_team_id_abbrev(team_name):
    nba_teams = teams.get_teams()
    temp_team = [team for team in nba_teams if team['abbreviation'] == team_name][0]
    return temp_team['id']

# Returns DataFrame of latest game
def get_latest_game(teamID):
    teamGameLog = teamgamelog.TeamGameLog(team_id=teamID)
    return teamGameLog.get_data_frames()[0].iloc[0]

# Boolean to check if the team played a game provided by the day offset
def did_play_yesterday(teamID):
    teamGameLog = teamgamelog.TeamGameLog(team_id=teamID)

    # Get the latest game date by the latest game DataFrame
    latest_game_date = get_latest_game(teamID)['GAME_DATE']

    # Format the date to be compatible with the API using pandas (!!!)
    formatted_date = pd.to_datetime(latest_game_date)

    # Sourcery being a GOAT (!!!)
    return (formatted_date == pd.Timestamp(date.today()) - timedelta(days=2))

# Need to work on an interface, or if I'm just going to pass the abbreviation through the command line


# Gets team data for the frame
abbreviation = 'CLE'
teamID = get_team_id_abbrev(abbreviation)
teamGameLog = teamgamelog.TeamGameLog(team_id=teamID)
latest_game = get_latest_game(teamID)
latest_game_ID = latest_game['Game_ID']

# If the team played yesterday, get the box score
if did_play_yesterday(teamID):
    boxScoreFrames = box_score.BoxScoreTraditionalV2(game_id=latest_game_ID)
else:
    print('No game yesterday')
    exit()

# Grabbing the first dataframe from the get_data_frames() function, which is the box score
df = boxScoreFrames.get_data_frames()[0]

# teamdf = testBoxScore.get_data_frames()[1]
# print(teamdf)

# Dropping NaN values (Coach's decisions to not play)
df = df.dropna()

# Dropping columns that aren't needed
dropped_columns = ['COMMENT', 'MIN', 'NICKNAME', 'TEAM_CITY', 'START_POSITION', 'GAME_ID', 'PLAYER_ID']
for column in dropped_columns:
    df = df.drop([column], axis='columns')

# Converting the floats to ints where they are needed
cleaned_columns = ['PTS', 'PLUS_MINUS', 'PF', 'TO', 'BLK', 'STL', 'AST', 'REB', 'DREB', 'OREB', 'FTA', 'FTM', 'FG3A', 'FG3M', 'FGA', 'FGM']
for column in cleaned_columns:
    df[[column]] = df[[column]].apply(np.int64)

# Finding max value in a given column
def max_value(column):
    return df[column].max()

# Finding the index of the max value in a given column
def max_value_index(column):
    return df[column].idxmax()

def player_attribute_leader(column):
    returnString = ''
    columnMax = df[column].max()
    columnMaxIndex = df[column].idxmax()
    playerName = df.loc[columnMaxIndex, 'PLAYER_NAME']
    returnString += f'({column}) {playerName}: ' + str(columnMax)
    return returnString


df = df.loc[df['TEAM_ABBREVIATION'] == abbreviation]
pointsLeader = player_attribute_leader('PTS')
#print(pointsLeader)

leader_attributes = ['PTS', 'AST', 'REB', 'STL', 'BLK', 'TO']

for attribute in leader_attributes: 
    tempLeader = player_attribute_leader(attribute)
    print(tempLeader)

#print(pointsMax)
#print(pointsMaxIndex)

# Delete rows that do not have the team abbreviation 

print(df)

#print(df)

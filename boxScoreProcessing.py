from datetime import date, timedelta, datetime
from hashlib import new
from matplotlib.pyplot import get
from nba_api.stats.endpoints import teamgamelog, boxscoretraditionalv2 as box_score, boxscoresummaryv2 as team_scoring

from nba_api.stats.static import teams, players

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os
import plotly.graph_objects as go


def get_team_id_abbrev(team_name):
    '''
    Returns the ID of the team designated by the abbreviation
    '''
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
    return (formatted_date == pd.Timestamp(date.today()) - timedelta(days=1))


# Gets the player that was the attribute leader in a certain category
def player_attribute_leader(column, df):
    returnString = ''
    columnMax = df[column].max()
    columnMaxIndex = df[column].idxmax()
    playerName = df.loc[columnMaxIndex, 'PLAYER_NAME']
    returnString += f'({column}) {playerName}: ' + str(columnMax)
    return returnString


# Throwing out columns that are not needed, as well as players that did not play (comes up as NaN)
def clean_df(df):
    df = df.dropna()
    return df


def drop_columns(dropped_columns, df):
    for column in dropped_columns:
        df = df.drop([column], axis='columns')
    return df


def clean_columns(cleaned_columns, df):
    for column in cleaned_columns:
        df[[column]] = df[[column]].apply(np.int64)
    return df


def get_latest_game_ID(teamID):
    teamGameLog = teamgamelog.TeamGameLog(team_id=teamID)
    latest_game = get_latest_game(teamID)
    return latest_game['Game_ID']


if __name__ == '__main__':

    # Team we're getting info for
    abbreviation = 'LAL'

    # Get the team ID
    teamID = get_team_id_abbrev(abbreviation)
    latest_game_ID = get_latest_game_ID(teamID)

    

    # If the team played yesterday, get the box score
    if did_play_yesterday(teamID):
        boxScoreFrames = box_score.BoxScoreTraditionalV2(game_id=latest_game_ID)
    else:
        print('No game yesterday')
        exit()

    # Getting the second dataframe, which is team data
    teamBoxScore = boxScoreFrames.get_data_frames()[1]

    # Dropping columns that are not needed
    dropped_columns = ['GAME_ID', 'TEAM_ID', 'TEAM_CITY', 'MIN', 'PF', 'PLUS_MINUS', 'TEAM_ABBREVIATION']
    teamBoxScore = drop_columns(dropped_columns, teamBoxScore)

    # Grabbing the first dataframe from the get_data_frames() function, which is the box score
    playerBoxScore = boxScoreFrames.get_data_frames()[0]

    # Dropping columns that are not needed
    dropped_columns = ['COMMENT', 'NICKNAME', 'TEAM_CITY', 'START_POSITION', 'GAME_ID', 'PLAYER_ID', 'TEAM_ID', 'PLUS_MINUS', 'OREB', 'DREB', 'FT_PCT', 'FG3_PCT', 'FG_PCT', 'PF']
    playerBoxScore = drop_columns(dropped_columns, playerBoxScore)

    # Converting the floats to ints where they are needed
    cleaned_columns = ['PTS', 'TO', 'BLK', 'STL', 'AST', 'REB', 'FTA', 'FTM', 'FG3A', 'FG3M', 'FGA', 'FGM']
    playerBoxScore = clean_columns(cleaned_columns, playerBoxScore)

    playerBoxScore = clean_df(playerBoxScore)

    teamScoreFrames = team_scoring.BoxScoreSummaryV2(game_id=latest_game_ID)
    teamScoring = teamScoreFrames.get_data_frames()[5]

    dropped_columns = ['GAME_DATE_EST', 'GAME_SEQUENCE', 'GAME_ID', 'TEAM_ID', 'TEAM_CITY_NAME', 'TEAM_NICKNAME', 'TEAM_WINS_LOSSES']
    teamScoring = drop_columns(dropped_columns, teamScoring)

    # Drop columns that have zero (OTs past like 2)
    teamScoring = teamScoring.loc[:, (teamScoring != 0).any(axis=0)]

    # Changing the 'TEAM_ABBREVIATION' column to 'TEAM'
    teamScoring.rename(columns={'TEAM_ABBREVIATION': 'TEAM'}, inplace=True)

    # Delete rows that do not have the team abbreviation
    playerBoxScore = playerBoxScore.loc[playerBoxScore['TEAM_ABBREVIATION'] == abbreviation]

    #print(teamBoxScore)
    #print('\n')
    #print(playerBoxScore)
    #print('\n')
    print(teamScoring)

    leader_attributes = ['PTS', 'AST', 'REB', 'STL', 'BLK', 'TO', 'FG3M']

    for attribute in leader_attributes:
        leader = player_attribute_leader(attribute, playerBoxScore)
        #print(leader)

# WORK IN PROGRESS working on converting data to a viewable table that is then sent to an image
df = teamBoxScore

fig = go.Figure(data=[go.Table(
    header=dict(values=list(df.columns),
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=df.transpose().values.tolist(),
            fill_color='lavender',
            align='left'))
])

df = teamScoring

fig = go.Figure(data=[go.Table(
    header=dict(values=list(df.columns),
                fill_color='mediumorchid',
                align='left'),
    cells=dict(values=df.transpose().values.tolist(),
            fill_color='gold',
            align='left'))
])

fig.show()

# Creating an image directory and putting the images in it
#if not os.path.exists("images"):
    #os.mkdir("images")
# fig.write_image("images/table.png")

# I have all the information mostly, that I need for a email. Now just need to figure out how to format the data

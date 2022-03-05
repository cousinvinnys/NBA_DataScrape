#!/usr/bin/env python
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

import json

from nbaAPIAccessor import nbaAPIAccessor


def get_team_id_abbrev(team_name):
    '''
    Returns the ID of the team designated by the abbreviation provided
    '''
    nba_teams = teams.get_teams()
    temp_team = [team for team in nba_teams if team['abbreviation'] == team_name][0]
    return temp_team['id']


def get_latest_game(teamID):
    '''
    Returns DataFrame of latest game
    '''
    teamGameLog = teamgamelog.TeamGameLog(team_id=teamID)
    return teamGameLog.get_data_frames()[0].iloc[0]


def did_play_when(teamID, days_ago):
    '''
    Returns True if the team played yesterday, False if not.
    Date/Time is formatted to be compatible with pandas, and then
    compared.
    '''
    teamGameLog = teamgamelog.TeamGameLog(team_id=teamID)
    latest_game_date = get_latest_game(teamID)['GAME_DATE']
    formatted_date = pd.to_datetime(latest_game_date)

    # Sourcery being a GOAT (!!!)
    return (formatted_date == pd.Timestamp(date.today()) - timedelta(days=days_ago))


def player_attribute_leader(column, df):
    '''
    Returns the player that was the attribute leader in a certain category
    '''
    returnString = ''
    columnMax = df[column].max()
    columnMaxIndex = df[column].idxmax()
    playerName = df.loc[columnMaxIndex, 'PLAYER_NAME']
    returnString += f'({column}) {playerName}: ' + str(columnMax)
    return returnString


def clean_df(df):
    '''
    Returns a cleaned DataFrame
    '''
    df = df.dropna()
    return df


def drop_columns(dropped_columns, df):
    '''
    Returns a DataFrame with the columns (in an array) dropped
    '''
    for column in dropped_columns:
        df = df.drop([column], axis='columns')
    return df


def convert_column_to_int(cleaned_columns, df):
    '''
    Returns a DataFrame with the columns (in an array) converted to int
    '''
    for column in cleaned_columns:
        df[[column]] = df[[column]].apply(np.int64)
    return df


def get_latest_game_ID(teamID):
    '''
    Returns the ID of the latest game
    '''
    teamGameLog = teamgamelog.TeamGameLog(team_id=teamID)
    latest_game = get_latest_game(teamID)
    return latest_game['Game_ID']


def get_team_color(abbreviation):
    '''
    Returns the color of the team
    '''
    with open('team_colors.json') as f:
        return json.load(f)[abbreviation]


if __name__ == '__main__':

    abbreviation = 'CLE'
    teamID = get_team_id_abbrev(abbreviation)
    latest_game_ID = get_latest_game_ID(teamID)

    if did_play_when(teamID, 1):
        boxScoreFrames = box_score.BoxScoreTraditionalV2(game_id=latest_game_ID)
    else:
        print('No game yesterday')
        exit()

    accessor = nbaAPIAccessor()
    #frames = accessor.testFunc("testing asap rocky")
    #print(frames)

    teamScoreFrames = team_scoring.BoxScoreSummaryV2(game_id=latest_game_ID)
    teamScoring = teamScoreFrames.get_data_frames()[5]
    dropped_columns = ['GAME_DATE_EST', 'GAME_SEQUENCE', 'GAME_ID', 'TEAM_ID', 'TEAM_CITY_NAME',
                       'TEAM_NICKNAME', 'TEAM_WINS_LOSSES']
    teamScoring = drop_columns(dropped_columns, teamScoring)
    teamScoring = teamScoring.loc[:, (teamScoring != 0).any(axis=0)]
    teamScoring.rename(columns={'PTS_QTR1': 'QTR1', 'PTS_QTR2': 'QTR2', 'PTS_QTR3': 'QTR3', 'PTS_QTR4': 'QTR4'}, inplace=True)
    teamScoring.rename(columns={'TEAM_ABBREVIATION': 'TEAM'}, inplace=True)


    teamBoxScore = boxScoreFrames.get_data_frames()[1]
    dropped_columns = ['GAME_ID', 'TEAM_ID', 'TEAM_CITY', 'MIN', 'PF', 'PLUS_MINUS', 'TEAM_ABBREVIATION', 'FG_PCT', 'FG3_PCT', 'FT_PCT']
    teamBoxScore = drop_columns(dropped_columns, teamBoxScore)
    teamBoxScore.rename(columns={'TEAM_NAME': 'TEAM'}, inplace=True)


    playerBoxScore = boxScoreFrames.get_data_frames()[0]
    dropped_columns = ['COMMENT', 'NICKNAME', 'TEAM_CITY', 'START_POSITION', 'GAME_ID', 'PLAYER_ID',
                       'TEAM_ID', 'PLUS_MINUS', 'OREB', 'DREB', 'FT_PCT', 'FG3_PCT', 'FG_PCT', 'PF']
    playerBoxScore = drop_columns(dropped_columns, playerBoxScore)
    cleaned_columns = ['PTS', 'TO', 'BLK', 'STL', 'AST', 'REB', 'FTA', 'FTM', 'FG3A', 'FG3M', 'FGA', 'FGM']
    playerBoxScore = convert_column_to_int(cleaned_columns, playerBoxScore)
    playerBoxScore = clean_df(playerBoxScore)
    teamScoreOnly = playerBoxScore.loc[playerBoxScore['TEAM_ABBREVIATION'] == abbreviation]


    leader_attributes = ['PTS', 'AST', 'REB', 'STL', 'BLK', 'TO', 'FG3M']
    for attribute in leader_attributes:
        leader = player_attribute_leader(attribute, teamScoreOnly)
        print(leader)

    print('\n', teamScoring, '\n\n', teamBoxScore, '\n\n', playerBoxScore)


# WORK IN PROGRESS working on converting data to a viewable table that is then sent to an image
df = teamScoreOnly

color = get_team_color(abbreviation)

fig = go.Figure(data=[go.Table(
    columnwidth=[500, 500],
    header=dict(values=list(df.columns),
                fill_color=color[0],
                align='left'),
    cells=dict(values=df.transpose().values.tolist(),
               fill_color=color[1],
               align='left'))
])

fig.update_layout(width=1250, height=500)
fig.show()

# Blackbox function inside NBA API Accessor class
# Get team colors for each team, input into json file
# Format tables


# fig = go.Figure(data=[go.Table(
#     header=dict(values=list(df.columns),
#                 fill_color='mediumorchid',
#                 align='left'),
#     cells=dict(values=df.transpose().values.tolist(),
#             fill_color='gold',
#             align='left'))
# ])

# #fig.show()

# df = playerBoxScore

# fig = go.Figure(data=[go.Table(
#     header=dict(values=list(df.columns),
#                 fill_color='mediumorchid',
#                 align='left'),
#     cells=dict(values=df.transpose().values.tolist(),
#             fill_color='gold',
#             align='left'))
# ])

# fig.show()

# Creating an image directory and putting the images in it
# if not os.path.exists("images"):
# os.mkdir("images")
# fig.write_image("images/table.png")

# I have all the information mostly, that I need for a email. Now just need to figure out how to format the data

from nba_api.stats.endpoints import playergamelog
from nba_api.stats.endpoints import teamgamelog
from nba_api.stats.endpoints import boxscoretraditionalv2 as box_score
import pandas as pd
import numpy as np

from nba_api.stats.static import teams
from nba_api.stats.static import players

testBoxScore = box_score.BoxScoreTraditionalV2(game_id='0022100825')
df = testBoxScore.get_data_frames()[0]

dropped_columns = ['COMMENT', 'MIN', 'NICKNAME', 'TEAM_CITY', 'START_POSITION']

for column in dropped_columns:
    df = df.drop([column], axis='columns')

df = df.drop([12], axis='rows')


# df = df.astype({"PTS": 'int', ""})

cleaned_columns = ['PTS', 'PLUS_MINUS', 'PF', 'TO', 'BLK', 'STL', 'AST', 'REB', 'DREB', 'OREB', 'FTA', 'FTM', 'FG3A', 'FG3M', 'FGA', 'FGM']

for column in cleaned_columns:
    df[[column]] = df[[column]].apply(np.int64)



print(df)
# print(df.columns)


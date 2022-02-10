from nba_api.stats.endpoints import playergamelog
from nba_api.stats.endpoints import teamgamelog
from nba_api.stats.endpoints import boxscoreplayertrackv2 as box_score
import pandas as pd

from nba_api.stats.library.parameters import SeasonAll
from nba_api.stats.static import teams
from nba_api.stats.static import players

testBoxScore = box_score.BoxScorePlayerTrackV2(game_id='0022100825')
df = testBoxScore.get_data_frames()[0]


# print(df)
# print(df.iloc[[4]])
# print(df.columns)
# print(df.loc[[4]])

test = df["TEAM_CITY"]
# print(test)

test3 = df[["PLAYER_NAME", "RBC", "AST", "CFG_PCT"]]
# print(test3)

editedDF = df.drop(["START_POSITION", "SPD", "COMMENT", "TCHS", "DIST", "SAST", "FTAST", "PASS", "GAME_ID", "TEAM_ID", "TEAM_CITY"], axis='columns')
print(editedDF)
# print(df.info())
# print(df['PLAYER_NAME'])



# LeBron's game logs from 2018-2019 season
# gamelog_bron = playergamelog.PlayerGameLog(player_id='2544', season = '2018')

# Converts gamelog object into a pandas dataframe, can also be JSON or dictionary
# df_bron_games_2018 = gamelog_bron.get_data_frames()

# All of LeBron's game logs
# gamelog_bron_all = playergamelog.PlayerGameLog(player_id='2544', season = SeasonAll.all)

# Dataframe of all of LeBron's game logs
# df_bron_games_all = gamelog_bron_all.get_data_frames()
# print(df_bron_games_all)

nba_teams = teams.get_teams()

# Identify the team object for the Cavs by abbreviation CLE
cavs = [team for team in nba_teams if team['abbreviation'] == 'CLE'][0]

# Exteracting the ID from the team object 
cavsID = cavs['id']

# Cavs gamelog from this season
cavs_gamelog = teamgamelog.TeamGameLog(team_id=cavsID)

# Need single game meta-information
cavs_gamelog_single = cavs_gamelog.get_data_frames()

# print(cavs_gamelog.get_data_frames())



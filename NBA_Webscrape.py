# First we import the endpoint
# We will be using pandas dataframes to manipulate the data
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.endpoints import teamgamelog


import pandas as pd

#Call the API endpoint passing in lebron's ID & which season
gamelog_bron = playergamelog.PlayerGameLog(player_id='2544', season = '2018')

#Converts gamelog object into a pandas dataframe
#can also convert to JSON or dictionary
df_bron_games_2018 = gamelog_bron.get_data_frames()

# If you want all seasons, you must import the SeasonAll parameter
from nba_api.stats.library.parameters import SeasonAll
from nba_api.stats.static import teams

nba_teams = teams.get_teams()
cavs = [team for team in nba_teams if team['abbreviation'] == 'CLE'][0]
cavsID = cavs['id']

gamelog_bron_all = playergamelog.PlayerGameLog(player_id='2544', season = SeasonAll.all)



cavs_gamelog = teamgamelog.TeamGameLog(team_id=cavsID)

print(cavs_gamelog.get_data_frames())

df_bron_games_all = gamelog_bron_all.get_data_frames()

# print(df_bron_games_all)
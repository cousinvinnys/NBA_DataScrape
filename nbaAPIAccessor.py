# Class for Accessing dataframes
from nba_api.stats.endpoints import teamgamelog, boxscoretraditionalv2 as box_score, boxscoresummaryv2 as team_scoring
from nba_api.stats.static import teams, players


class nbaAPIAccessor:

    def get_latest_game(self, teamID):
        '''
        Returns DataFrame of latest game
        '''
        teamGameLog = teamgamelog.TeamGameLog(team_id=teamID)
        return teamGameLog.get_data_frames()[0].iloc[0]

    def get_latest_game_ID(self, teamID):
        '''
        Returns the ID of the latest game
        '''
        teamGameLog = teamgamelog.TeamGameLog(team_id=teamID)
        latest_game = self.get_latest_game(teamID)
        return latest_game['Game_ID']

    def getBoxScoreFrames(self, teamID):
        return box_score.BoxScoreTraditionalV2(game_id=self.get_latest_game_ID(teamID))


    def getTeamBoxScore(self, teamID):
        teamBoxScore = self.getBoxScoreFrames.get_data_frames()[1]
        dropped_columns = ['GAME_ID', 'TEAM_ID', 'TEAM_CITY', 'MIN', 'PF', 'PLUS_MINUS', 'TEAM_ABBREVIATION', 'FG_PCT', 'FG3_PCT', 'FT_PCT']
        teamBoxScore = drop_columns(dropped_columns, teamBoxScore)
        teamBoxScore.rename(columns={'TEAM_NAME': 'TEAM'}, inplace=True)

    def drop_columns(dropped_columns, df):
        '''
        Returns a DataFrame with the columns (in an array) dropped
        '''
        for column in dropped_columns:
            df = df.drop([column], axis='columns')
        return df

    def testFunc(self, piss):
        return piss
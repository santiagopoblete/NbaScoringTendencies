import pandas as pd

# Read the CSV file
lineScore = pd.read_csv('./csv/line_score.csv')
games = pd.read_csv('./csv/game.csv')

# Get the column names and row count
column_names = lineScore.columns.tolist()
row_count = lineScore.shape[0]

print(column_names, row_count)

# Remove all rows that dont have a value in any quarter
lineScore = lineScore.dropna(subset=['pts_qtr1_home', 'pts_qtr1_away', 'pts_qtr2_home', 'pts_qtr2_away', 'pts_qtr3_home', 'pts_qtr3_away', 'pts_qtr4_home', 'pts_qtr4_away'])

# Get points by third quarter
ptsQtr3Home = lineScore['pts_qtr3_home'] + lineScore['pts_qtr2_home'] + lineScore['pts_qtr1_home']
ptsQtr3Away = lineScore['pts_qtr3_away'] + lineScore['pts_qtr2_away'] + lineScore['pts_qtr1_away']

# Remove games where differential is less than 10 points
lineScore = lineScore[abs(ptsQtr3Home - ptsQtr3Away) > 10]

# Get points by fourth quarter of remaining games
ptsQtr4Home = lineScore['pts_home']
ptsQtr4Away = lineScore['pts_away']

# Get all ids ('game_id') from games where the team that was losing in the third quarter won the game
homeWinningTeams = lineScore[(ptsQtr3Home < ptsQtr3Away) & (ptsQtr4Home > ptsQtr4Away)]
awayWinningTeams = lineScore[(ptsQtr3Home > ptsQtr3Away) & (ptsQtr4Home < ptsQtr4Away)]
homeWinningTeamIds = homeWinningTeams['game_id']
awayWinningTeamsIds =  awayWinningTeams['game_id']
winningTeamIds = pd.concat([homeWinningTeamIds, awayWinningTeamsIds])

# Get matching games from games dataframe
comebackGames = games[games['game_id'].isin(winningTeamIds)]
comebackGamesIds = comebackGames['game_id']
print(comebackGamesIds.head(5))

# remove games where no 3pt attempts were made
comebackGames = comebackGames.dropna(subset=['fg3a_home', 'fg3a_away'])


# Get avg 3pt attempts
avgThreePtAttemptsHome = comebackGames['fg3a_home'].mean()
avgThreePtAttemptsAway = comebackGames['fg3a_away'].mean()

print(avgThreePtAttemptsHome, avgThreePtAttemptsAway)

# Get 3pt attempts
threePtAttemptsHome = comebackGames['fg3a_home']
threePtAttemptsAway = comebackGames['fg3a_away']

# top 5 results of 3pt percentage and 3pt made
print(threePtAttemptsHome.head(5))
print(threePtAttemptsAway.head(5))
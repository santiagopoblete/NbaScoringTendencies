import pandas as pd

# Read the CSV file
df = pd.read_csv('./archive/games.csv')
teamNames = pd.read_csv('./archive/teams.csv')

# Get the column names and row count
column_names = df.columns.tolist()
row_count = df.shape[0]

print(column_names, row_count)

# Getting point differential for each game played
df['point_diff'] = df['PTS_home'] - df['PTS_away']

# Getting the winer of the game
df['WINNER'] = df['HOME_TEAM_WINS'].apply(lambda x: 'HOME_TEAM' if x == 1 else 'VISITOR_TEAM')

# Select relevant columns
pointDiffTeams = df[['point_diff', 'HOME_TEAM_ID', 'VISITOR_TEAM_ID', 'WINNER', 'GAME_DATE_EST']]

# Get 20 highest point differentials
highest_point_diff = pointDiffTeams.nlargest(20, 'point_diff')

# Replacing team IDs with team names
highest_point_diff = highest_point_diff.replace({'HOME_TEAM_ID': teamNames.set_index('TEAM_ID')['NICKNAME']})
highest_point_diff = highest_point_diff.replace({'VISITOR_TEAM_ID': teamNames.set_index('TEAM_ID')['NICKNAME']})

#Adding a new column to show the winning team and the year
highest_point_diff['WINNING_TEAM'] = highest_point_diff['WINNER']
highest_point_diff['YEAR'] = highest_point_diff['GAME_DATE_EST'].str[:4]



print(highest_point_diff)
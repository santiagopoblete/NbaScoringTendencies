import pandas as pd
import matplotlib.pyplot as plt

# import game data

games = pd.read_csv('./csv/game.csv')

# remove games with missing data

games = games.dropna(subset=['fg3_pct_home', 'fg3_pct_away'])

# remove games previous to 1979

games = games[games['game_date'] > '1979-01-01 00:00:00']

# Get average sum of 3pt percentage per year

games['game_date'] = pd.to_datetime(games['game_date'])

games['year'] = games['game_date'].dt.year

avg_3pt_percentage = games.groupby('year').agg({'fg3_pct_home':'mean', 'fg3_pct_away':'mean'}).reset_index()

avg_3pt_percentage['avg3pt_percentage'] = (avg_3pt_percentage['fg3_pct_home'] + avg_3pt_percentage['fg3_pct_away'])/2

# Export modified csv

avg_3pt_percentage.to_csv('./csv/avg_3pt_percentage.csv', index=False)

# plot average 3pt percentage per year

plt.plot(avg_3pt_percentage['year'], avg_3pt_percentage['avg3pt_percentage'])

plt.xlabel('Year')

plt.ylabel('Average 3pt percentage')

plt.title('Average 3pt percentage per year')

plt.savefig('./photos/avg3ptpercentageCSVTEST.png')
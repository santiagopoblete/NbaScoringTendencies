import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

import numpy as np

# import game data

games = pd.read_csv('./csv/game.csv')

# remove games with missing data

games = games.dropna(subset=['fg3a_home', 'fg3a_away', 'fg3_pct_home', 'fg3_pct_away', 'pts_home', 'pts_away'])

# remove games previous to 1979

games = games[games['game_date'] > '1979-01-01 00:00:00']

# Get average sum of 3pt percentage per year

games['game_date'] = pd.to_datetime(games['game_date'])

games['year'] = games['game_date'].dt.year

avg_3pt_percentage = games.groupby('year').agg({'fg3_pct_home':'mean', 'fg3_pct_away':'mean'}).reset_index()

avg_3pt_percentage['avg3pt_percentage'] = (avg_3pt_percentage['fg3_pct_home'] + avg_3pt_percentage['fg3_pct_away'])/2


# plot average 3pt percentage per year

plt.plot(avg_3pt_percentage['year'], avg_3pt_percentage['avg3pt_percentage'])

plt.xlabel('Year')

plt.ylabel('Average 3pt percentage')

plt.title('Average 3pt percentage per year')

plt.legend(['Average 3pt percentage', 'Exponential fit'])


plt.show()

plt.savefig('./photos/avg3ptpercentage.png')

plt.close()
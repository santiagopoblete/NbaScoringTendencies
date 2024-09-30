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

# Add new column with the that goes from 1 to the number of years

avg_3pt_percentage['year_number'] = range(1, len(avg_3pt_percentage) + 1)

# Logarithmic fit

x = avg_3pt_percentage['year_number'].values.reshape(-1, 1)

y = avg_3pt_percentage['avg3pt_percentage'].values

model = LinearRegression()

model.fit(np.log(x), y)

avg_3pt_percentage['log_fit'] = model.predict(np.log(x))

# Polynomial fit

x = avg_3pt_percentage['year_number'].values.reshape(-1, 1).flatten()

print(x)

y = avg_3pt_percentage['avg3pt_percentage'].values

print(y)

poly_fit = np.polyfit(x, y, 6)

avg_3pt_percentage['poly_fit'] = np.polyval(poly_fit, x)

print(avg_3pt_percentage['poly_fit'])

# R2 score for each fit

r2_log = round(r2_score(y, avg_3pt_percentage['log_fit']),2)

r2_poly = round(r2_score(y, avg_3pt_percentage['poly_fit']), 2)

print(f'R2 score for logarithmic fit: {r2_log}')

print(f'R2 score for polynomial fit: {r2_poly}')

# plot average 3pt percentage per year

plt.plot(avg_3pt_percentage['year'], avg_3pt_percentage['avg3pt_percentage'], label='Average 3pt percentage')

plt.plot(avg_3pt_percentage['year'], avg_3pt_percentage['log_fit'], label='Logarithmic fit')

plt.plot(avg_3pt_percentage['year'], avg_3pt_percentage['poly_fit'], label='Polynomial fit')

plt.xlabel('Year')

plt.ylabel('Average 3pt percentage')

plt.title('Average 3pt percentage per year')

# Add R2 scores to the plot

plt.text(1995, 0.30, f'R2 score for logarithmic fit: {r2_log}', fontsize=12)

plt.text(1995, 0.25, f'R2 score for polynomial fit: {r2_poly}', fontsize=12)

plt.legend()

plt.savefig('./photos/avg3ptpercentage2.png')

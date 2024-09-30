import os
import datetime

import IPython
import IPython.display
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import tensorflow as tf

mpl.rcParams['figure.figsize'] = (8, 6)
mpl.rcParams['axes.grid'] = False

# import game data
games = pd.read_csv('././csv/game.csv')

print(games.head())

# Split games per year
games['game_date'] = pd.to_datetime(games['game_date'])
games['year'] = games['game_date'].dt.year

# remove games previous to 1979

games = games[games['game_date'] > '1979-01-01 00:00:00']

# drop all columns that are from playoffs

games = games[games['season_type'] == 'Regular Season']

# remove columns that are not needed

games = games.drop(columns=['season_id', 'team_abbreviation_home', 'team_abbreviation_away', 'matchup_home', 'matchup_away', 'video_available_home', 'video_available_away', 'season_type'])


# remove games with missing data
games = games.dropna(subset=['fg3a_home', 'fg3a_away', 'fg3_pct_home', 'fg3_pct_away', 'pts_home', 'pts_away'])

# turn all 3pt% and attempts from both teams into a single average column

games['3P%'] = games['fg3_pct_home'] + games['fg3_pct_away'] / 2

games['3P_attempts'] = games['fg3a_home'] + games['fg3a_away'] / 2

# remove columns that are not needed

games = games.drop(columns=['fg3_pct_home', 'fg3_pct_away', 'fg3a_home', 'fg3a_away'])

# remove games with missing data

games = games.dropna(subset=['3P%', '3P_attempts'])

# Column indices

column_indices = {name: i for i, name in enumerate(games.columns)}
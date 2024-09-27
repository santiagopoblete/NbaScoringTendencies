import pandas as pd
import matplotlib.pyplot as plt

# import game data
games = pd.read_csv('./csv/game.csv')

# remove games with missing data
games = games.dropna(subset=['fg3a_home', 'fg3a_away', 'fg3_pct_home', 'fg3_pct_away', 'pts_home', 'pts_away'])

# remove games previous to 1979

games = games[games['game_date'] > '1979-01-01 00:00:00']


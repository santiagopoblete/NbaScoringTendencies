import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# import game data

games = pd.read_csv('./csv/game.csv')

# remove blank columns

games = games.iloc[:,0:55]

# Remove games previous to the 3 point line era (1980 onwards)

games = games[games['game_date'] > '1980-01-01 00:00:00']

# Split games per era (5 year span per era)

games['game_date'] = pd.to_datetime(games['game_date'])
games['year'] = games['game_date'].dt.year
games['year'] = games['year']//5*5

print(games.head())

# leave only relevant data for final score

games = games[['wl_home', 'min', 'fg_pct_home', 'fg3_pct_home', 'ft_pct_home', 'reb_home', 'ast_home', 'stl_home', 'blk_home', 'tov_home', 'pf_home', 'pts_home', 'wl_away', 'fg_pct_away', 'fg3_pct_away', 'ft_pct_away', 'reb_away', 'ast_away', 'stl_away', 'blk_away', 'tov_away', 'pf_away', 'pts_away', 'plus_minus_away']]

# remove games with missing data

games = games.dropna()

# verify if there are missing values

print(games.isnull().values.any())

print(games.head())

# Split data into two sets: home wins and home losses

games_wins = games[games['wl_home'] == 'W']
games_losses = games[games['wl_home'] == 'L']

# Split games_wins and games_losses into training and test sets

X_wins = games_wins[['reb_home', 'ast_home', 'stl_home', 'blk_home', 'tov_home', 'pf_home']].values

y_wins = games_wins['pts_home'].values

X_train_wins, X_test_wins, y_train_wins, y_test_wins = train_test_split(X_wins, y_wins, test_size=0.2, random_state=0)

X_losses = games_losses[['reb_away', 'ast_away', 'stl_away', 'blk_away', 'tov_away', 'pf_away']].values

y_losses = games_losses['pts_away'].values

X_train_losses, X_test_losses, y_train_losses, y_test_losses = train_test_split(X_losses, y_losses, test_size=0.2, random_state=0)

# Linear Regression Object

regressor_wins = LinearRegression()

regressor_losses = LinearRegression()

# Fit the model

regressor_wins.fit(X_train_wins, y_train_wins)

regressor_losses.fit(X_train_losses, y_train_losses)

# Labels

x_labels_win = ['reb_home', 'ast_home', 'stl_home', 'blk_home', 'tov_home', 'pf_home']

x_labels_loss = ['reb_away', 'ast_away', 'stl_away', 'blk_away', 'tov_away', 'pf_away']

c_label = ['Coefficient']

# Coefficients

coeff_df_wins = pd.DataFrame(regressor_wins.coef_, x_labels_win, c_label)
print(coeff_df_wins)

coeff_df_losses = pd.DataFrame(regressor_losses.coef_, x_labels_loss, c_label)
print(coeff_df_losses)
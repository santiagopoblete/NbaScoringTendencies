import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# import game data
games = pd.read_csv('./csv/game.csv')

# remove games with missing data
games = games.dropna(subset=['fg3a_home', 'fg3a_away', 'fg3_pct_home', 'fg3_pct_away', 'pts_home', 'pts_away'])

# remove games previous to 1979

games = games[games['game_date'] > '1979-01-01 00:00:00']

# Get average sum of 3pt attempts per year
games['game_date'] = pd.to_datetime(games['game_date'])
games['year'] = games['game_date'].dt.year

avg_3pt_attempts = games.groupby('year').agg({'fg3a_home':'mean', 'fg3a_away':'mean'}).reset_index()
avg_3pt_attempts['avg3pt_attempt'] = (avg_3pt_attempts['fg3a_home'] + avg_3pt_attempts['fg3a_away'])/2

# Linear Regression model with 3pt attempts as dependent variable and year as independent variable
X = avg_3pt_attempts['year'].values.reshape(-1,1)
y = avg_3pt_attempts['avg3pt_attempt'].values

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=0)

# Linear Regression Object
regressor = LinearRegression()

# Fit the model
regressor.fit(X_train, y_train)

# Labels

x_labels = ['Year']

# Calculate R2

r2 = r2_score(y, regressor.predict(X))

# Plot average 3pt attempts per year
plt.scatter(X, y, color='#00438c', marker='none')

plt.plot(avg_3pt_attempts['year'], avg_3pt_attempts['avg3pt_attempt'], color='#00438c')

plt.plot(X, regressor.predict(X),  color='#B8DE13', linestyle='--')

plt.xlabel('Año')
plt.ylabel('Intentos de 3 Puntos por Partido')
plt.title('Promedio Anual de Intentos de 3 Puntos por Partido')

plt.grid(True, linestyle='--', alpha=0.5, axis='y')

plt.show()
plt.savefig('./avg3ptAttemptsLinear.png')
plt.close()

# Print R2
print('R2:', r2)
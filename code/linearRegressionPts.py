import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# import game data

games = pd.read_csv('./csv/shotsAndWinsNba.csv')

# remove blank columns

games = games.iloc[:,0:19]

print(games.head())

# update wins 'W' to be % (multiply by 100 divide by 82)

games['W'] = games['W'] * 100 / 82

print(games.head())

# leave only relevant data for pts scored per game

games = games[['3P%','2FG%','W']]

# remove games with missing data

games = games.dropna()

# verify if there are missing values

print(games.isnull().values.any())

print(games.head())

# Get teams that have scored points

teams = games[games['W'] > 0]

# Split teams into training and test sets

X_teams = teams[['3P%','2FG%']].values

y_teams = teams['W'].values

X_train_wins, X_test_wins, y_train_wins, y_test_wins = train_test_split(X_teams, y_teams, test_size=0.4, random_state=0)

# Linear Regression Object

regressor_wins = LinearRegression()

# Fit the model

regressor_wins.fit(X_train_wins, y_train_wins)

# Labels

x_labels_teams = ['3P%','2P%']
c_label = ['Coefficient']

# Coefficients

coeff_df_wins = pd.DataFrame(regressor_wins.coef_, x_labels_teams, c_label)
print(coeff_df_wins)

# Predictions

y_pred_wins = regressor_wins.predict(X_test_wins)

# Residuals

residuals = pd.DataFrame({'Actual': y_test_wins, 'Predicted': y_pred_wins, 'Residuals': y_test_wins - y_pred_wins})
residuals = residuals.sample(n = 10)
residuals = residuals.sort_values(by='Actual')
print("residuals!! \n" ,residuals)

# R2 Score

r2 = r2_score(y_test_wins, y_pred_wins)
print("r2 score!!! \n",r2)

# Plot
plt.scatter(X_test_wins[:,0], y_test_wins, color='red', label='Actual') # indicamos los datos reales
plt.scatter(X_test_wins[:,0], y_pred_wins, color='blue', label='Predicted') # indicamos los datos de predicción

plt.title("Prediction of Wins based on 3P%") # indicamos el título del gráfico

plt.xlabel("3P%") # indicamos la etiqueta del eje de las x

plt.ylabel("Victories") # indicamos la etiqueta del eje de las y

plt.legend(loc='upper left') # indicamos la posición de la etiqueta de los datos

plt.savefig('linearRegressionPts.png') # guardamos el gráfico como una imagen
#The purpose of this file is to find which variables contribute for a higher 3p% in teams

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score


# import game data

games = pd.read_csv('./csv/teams_23_24.csv')

# remove blank columns

games = games.iloc[:,0:27]

print(games.head())

# Leave only important data for 3P%

games = games[['3P%','FT%','OREB','DREB','AST','STL','BLK','PFD']]

# remove games with missing data

games = games.dropna()

# verify if there are missing values

print(games.isnull().values.any())

# Find correlation between variables

correlation = games.corr()

print(correlation)

# Plot correlation matrix

plt.matshow(correlation)
plt.xticks(range(len(correlation.columns)), correlation.columns)
plt.yticks(range(len(correlation.columns)), correlation.columns)
plt.colorbar()
plt.show()
plt.savefig('./variables.png')
plt.close()

# Linear regression model with 3P% as dependent variable and OREB, DREB, BLK, AST, FT% as independent variables

X = games[['FT%','OREB','DREB','AST','BLK']].values

y = games['3P%'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=0)

regressor = LinearRegression()

regressor.fit(X_train, y_train)

print(regressor.coef_)

y_pred = regressor.predict(X_test)

df = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})

# Plot actual vs predicted values

plt.scatter(X_test[:,0], y_test, color='red', label='Actual') # indicamos los datos reales
plt.scatter(X_test[:,0], y_pred, color='blue', label='Predicted') # indicamos los datos de predicción


plt.xlabel('Actual')
plt.ylabel('Predicted')

plt.show()

plt.savefig('./3ptVariables.png')

plt.close()

# R2 Score

r2 = r2_score(y_test, y_pred)

print(r2)

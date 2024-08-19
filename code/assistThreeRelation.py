import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# import game data (data taken from https://www.kaggle.com/datasets/vivovinco/2023-2024-nba-player-stats?select=2023-2024+NBA+Player+Stats+-+Regular.csv)

players = pd.read_csv('./csv/playersStats_23_24.csv', encoding='latin-1')

# remove blank columns

players = players.iloc[:,0:30]

print(players.head()) 

# remove TOT stats

players = players[players['Tm'] != 'TOT']

# revome players not in top 100 with most assists per game

players = players.sort_values(by='AST', ascending=False)

playersAst = players.head(100)

players = players.sort_values(by='3P%', ascending=False)

players3P = players.head(100)

# get Tm of said players and count how many ocurrences are per team.

AstTeams = playersAst['Tm'].value_counts()
ThreePTeams = players3P['Tm'].value_counts()

tableAstThree = pd.concat([AstTeams, ThreePTeams], axis=1)

print(tableAstThree)

matplotlib_table = tableAstThree.plot(kind='bar', title='Teams with most players in top 100 in assists and 3P%',)
matplotlib_table.set_xlabel('Teams')
matplotlib_table.set_ylabel('Number of players')
matplotlib_table.legend(['Assists', '3P%'])
matplotlib_table.set_facecolor('DarkGrey')


plt.show()
plt.savefig('./assistThreeRelation.png')
plt.close()
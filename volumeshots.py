import pandas as pd
import matplotlib.pyplot as plt

# import game data
games = pd.read_csv('./csv/game.csv')

# remove games with missing data
games = games.dropna(subset=['fg3a_home', 'fg3a_away', 'fg3_pct_home', 'fg3_pct_away', 'pts_home', 'pts_away'])

# remove games previous to 1979

games = games[games['game_date'] > '1979-01-01 00:00:00']

# Split games per era (5 year span per era)
games['game_date'] = pd.to_datetime(games['game_date'])
games['year'] = games['game_date'].dt.year
games['year'] = games['year']//5*5


# get average sum of scores per 5 years
avg_scores = games.groupby('year').agg({'pts_home':'mean', 'pts_away':'mean'}).reset_index()
avg_scores['avgScore'] = (avg_scores['pts_home'] + avg_scores['pts_away'])/2

# get 3pt attempts and 3pt percentage per 5 years
games['fg3a_home'] = games['fg3a_home'].fillna(0)
games['fg3a_away'] = games['fg3a_away'].fillna(0)
games['fg3_pct_home'] = games['fg3_pct_home'].fillna(0)
games['fg3_pct_away'] = games['fg3_pct_away'].fillna(0)

avg_3pt_attempts = games.groupby('year').agg({'fg3a_home':'mean', 'fg3a_away':'mean'}).reset_index()
avg_3pt_attempts['avg3pt_attempt'] = (avg_3pt_attempts['fg3a_home'] + avg_3pt_attempts['fg3a_away'])/2

avg_3pt_percentage = games.groupby('year').agg({'fg3_pct_home':'mean', 'fg3_pct_away':'mean'}).reset_index()
avg_3pt_percentage['avg3pt_percentage'] = (avg_3pt_percentage['fg3_pct_home'] + avg_3pt_percentage['fg3_pct_away'])/2

# get 2pt attempts and 2pt percentage per 5 years, we have to remove 3pt attempts and 3pt percentage from total attempts and percentage
games['fga_home'] = games['fga_home'].fillna(0)
games['fga_away'] = games['fga_away'].fillna(0)
games['fg_pct_home'] = games['fg_pct_home'].fillna(0)
games['fg_pct_away'] = games['fg_pct_away'].fillna(0)

avg_2pt_attempts = games.groupby('year').agg({'fga_home':'mean', 'fga_away':'mean'}).reset_index()
avg_2pt_attempts['avg2pt_attempt'] = (avg_2pt_attempts['fga_home'] + avg_2pt_attempts['fga_away'])/2
avg_2pt_attempts['avg2pt_attempt'] = avg_2pt_attempts['avg2pt_attempt'] - avg_3pt_attempts['avg3pt_attempt']

avg_2pt_percentage = games.groupby('year').agg({'fg_pct_home':'mean', 'fg_pct_away':'mean'}).reset_index()
avg_2pt_percentage['avg2pt_percentage'] = ((avg_2pt_percentage['fg_pct_home'] - avg_3pt_percentage['fg3_pct_home']) + (avg_2pt_percentage['fg_pct_away'] - avg_3pt_percentage['fg3_pct_away']))/2


print("average scores")
print("-------------------------------------------")
print(avg_scores)
print("\n")
print("average 3pt attempts")
print("-------------------------------------------")
print(avg_3pt_attempts)
print("\n")
print("average 3pt percentage")
print("-------------------------------------------")
print(avg_3pt_percentage)
print("\n")

plt.plot(avg_scores['year'], avg_scores['avgScore'], label='Average of scores')
plt.savefig('average_scoring.png')
plt.close()

plt.plot(avg_3pt_attempts['year'], avg_3pt_attempts['avg3pt_attempt'], label='Average of 3pt attempts')
plt.savefig('average_3pt_att.png')
plt.close()

plt.plot(avg_3pt_percentage['year'], avg_3pt_percentage['avg3pt_percentage'], label='Average of 3pt percentage')
plt.savefig('average_3pt_per.png')
plt.close()

plt.plot(avg_2pt_attempts['year'], avg_2pt_attempts['avg2pt_attempt'], label='Average of 2pt attempts')
plt.savefig('average_2pt_att.png')
plt.close()

plt.plot(avg_2pt_percentage['year'], avg_2pt_percentage['avg2pt_percentage'], label='Average of 2pt percentage')
plt.savefig('average_2pt_per.png')
plt.close()


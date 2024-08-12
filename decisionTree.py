import pandas
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt

df = pandas.read_csv('./csv/someGameStats23_24.csv')
df = df.dropna()
df = df.iloc[:,1:7]

print(df.head())


features = ['3PT%', 'LESS', 'MORE', 'FT%', 'WTOTAL']

X = df[features]
y = df['NEXTW']

print(X)
print(y)

dtree = DecisionTreeClassifier()
dtree = dtree.fit(X, y)

tree.plot_tree(dtree, feature_names=features)
plt.savefig('dtree.png')    

print(dtree.predict([[36.1, 56.3, 45.5, 81.2, 21]]))
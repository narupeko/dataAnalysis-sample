import pandas as pd


#import csv
df = pd.read_csv('iris.csv')
print(df.dtypes)
print(df.head())

print(df.ix[:,3:].groupby('Species').mean())
print(df.ix[:,3:].groupby('Species').std())




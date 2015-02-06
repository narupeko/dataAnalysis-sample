
# よく使うDataframe周りのコードをまとめた
import pandas as pd

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


#import csv
df = pd.read_csv('iris.csv')
print(df.dtypes)
print(df.head())

print(df.ix[:,1:].groupby('Species').mean())
print(df.ix[:,1:].groupby('Species').std())
print(df.ix[:,2:].groupby('Species').agg(['mean','std','size']))


print(df[(df['Species']=='setosa') & (df['Sepal.Width']>4)]) #選択の仕方
print(df[(df['Species']=='setosa') & (df['Sepal.Width']>4)].sort('Sepal.Width',ascending=True) )#昇順
print(df[(df['Species']=='setosa') & (df['Sepal.Width']>4)].sort('Sepal.Width',ascending=False) ) #降順


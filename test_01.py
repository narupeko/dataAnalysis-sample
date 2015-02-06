

import pandas as pd
import scipy as sp

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


print(df[(df['Species']=='setosa') & (df['Sepal.Width']>4)]) #選択の仕方1
print(df[(df['Species']=='setosa') & (df['Sepal.Width']>4)].sort('Sepal.Width',ascending=True) )#昇順
print(df[(df['Species']=='setosa') & (df['Sepal.Width']>4)].sort('Sepal.Width',ascending=False) ) #降順


#functions=['mean','std','count']


#3項演算子
dayMean = 1.56
i =2
x = dayMean if i == 1 else dayMean*2 if i==2 else 5
print(x)

#変数選択
kakoDailyTextDic = {1:"{}の天気は{}です",2:["{}の降雨量は{}です"]}
#x = "hogehoge"
stateText = kakoDailyTextDic[1] .format("昨日の","晴れ")
print(stateText)


mix = lambda x,y: x +"。"+y
print(mix("hoge", "taro"))
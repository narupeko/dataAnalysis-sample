import pandas as pd

test= pd.Series([300,200,100,50,10])
print(test[1])
print(type(test))
print(len(test))
print(test[2])
print(test[3])

print(test[1]+test[2])
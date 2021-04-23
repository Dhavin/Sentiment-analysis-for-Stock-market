import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web

#style.use('ggplot')
f = input('Enter a Stock : ')

df = pd.read_csv("clusterdata/"+ f +"cluster.csv",index_col=0,encoding='latin-1')

def getstockvalue(change, followers, totalfollowers, polarity, confidence, currentprice):

    value = change*(followers/totalfollowers)*polarity*confidence/(currentprice)*10000
    print(value)
    return value

start = dt.datetime(2018,11,14)
end = dt.datetime(2019,11,14)

dk = web.DataReader("AAPL", "yahoo", start, end)
df.to_csv("ohlc/"+ f +".csv")
print(dk.tail(5))

currentprice = dk['Open'][0]
dif = abs(dk['Open'][0] - dk['Close'][0])
print(dif)

totalfollowers = df['followers'].sum()

for index,row in df.iterrows():
    followers = df['followers'][index]
    polarity = df['polarity'][index]
    confidence = df['sentiment_confidence'][index]
    df.at[index,'difference'] = getstockvalue(dif, followers, totalfollowers, polarity, confidence, currentprice)

df.to_csv("finaldata/"+ f+".csv")

print(df.head())

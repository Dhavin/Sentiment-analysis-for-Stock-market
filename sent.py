import textblob
import tweepy
import pandas
import sys
from textblob import TextBlob

#import trial6

consumer_key = 'j6pG1V3OYFuFZsazuj1Td0vt2'
consumer_secret = 'CesbfkzRpS7i8ZnaxVNAuDcdnFUy6tpwjYQsgKkHNbrlQaUXAN'
access_token = '1171755115629309953-Abto6o9LwDZB9Jvge38xSOX7rgSPpO'
access_token_secret = 'tA4AwYmGA7b5NmejOZbZ1HkshTEUKAU3pF1eBxwNFfjkI'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret,)
auth.set_access_token(access_token, access_token_secret)
f = input('Enter a Stock : ')
api = tweepy.API(auth)
colnames=['date', 'text', 'followers']

df = pandas.read_csv('tweetdata/'+ f +'tweets.csv',encoding='latin-1', names=colnames, header=None)
df['polarity'] = 0.0000
df['sentiment_confidence'] = 0.0000

for index,row in df.iterrows():
    analysis = TextBlob(df['text'][index])
    sentiment, confidence = analysis.sentiment
    df.at[index,'polarity'] = sentiment
    df.at[index,'sentiment_confidence'] = confidence

df.to_csv('sentimentdata/'+f +'sentiment.csv')
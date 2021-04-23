import tweepy
import csv
import sys
import datetime
import textblob
import tweepy
import pandas
from textblob import TextBlob
import pandas as pd
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
import glob

consumer_key = 'j6pG1V3OYFuFZsazuj1Td0vt2'
consumer_secret = 'CesbfkzRpS7i8ZnaxVNAuDcdnFUy6tpwjYQsgKkHNbrlQaUXAN'
access_token = '1171755115629309953-Abto6o9LwDZB9Jvge38xSOX7rgSPpO'
access_token_secret = 'tA4AwYmGA7b5NmejOZbZ1HkshTEUKAU3pF1eBxwNFfjkI'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

f = input('Enter a Stock tricker : ')

# Open/Create a file to append data
csvFile = open('tweetdata/'+f +'tweets.csv', 'a')
#Use csv Writer
fields = ('date','text', 'followers')
csvWriter = csv.writer(csvFile, lineterminator= '\n')

for tweet in tweepy.Cursor(api.search,q=f, lang="en", since_id="2018-2-23").items():
    print(tweet.created_at, tweet.text)
    follower_count = tweet.user.followers_count
    #if tweet.created_at >= datetime.datetime(2019,2,24):
    csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8'),follower_count])

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


f = input('Enter a Stock : ')
df = pd.read_csv('sentimentdata/'+ f +'sentiment.csv',index_col=0,
encoding='latin-1')
dfold = df
df = df.drop('text', 1)
print(df.head())
df = df.drop('date', 1)
print(df.head())

df_tr = df
# select proper number of clusters
'''
Y = df[['followers']]
X = df[['polarity']]

Nc = range(1, 20)
kmeans = [KMeans(n_clusters=i) for i in Nc]
score = [kmeans[i].fit(Y).score(Y) for i in range(len(kmeans))]
plt.plot(Nc,score)
plt.xlabel('Number of Clusters')
plt.ylabel('Score')
plt.title('Elbow Curve')
plt.show()
'''

# elbow plot showed the point of dropoff to be around 5 clusters

#Standardize

clmns = ['followers', 'polarity', 'sentiment_confidence']

df_tr_std= stats.zscore(df_tr[clmns])

#Clustering

kmeans = KMeans(n_clusters=5, random_state=0).fit(df_tr_std)
labels = kmeans.labels_

#Glue back to original data
df_tr['clusters']=labels
dfold['clusters']=labels

clmns.extend(['clusters'])

print(df_tr[clmns].groupby(['clusters']).mean())

#Scatter plot of polarity and confidence
sns.lmplot('polarity', 'sentiment_confidence',
           data=df_tr,
           fit_reg=False,
           hue="clusters",
           scatter_kws={"marker": "D",
                        "s": 20})

dfold.to_csv('clusterdata/'+ f +'cluster.csv')
plt.title('tweets grouped by polarity and sentiment_confidence')
plt.xlabel('polarity')
plt.ylabel('sentiment_confidences')
plt.show()

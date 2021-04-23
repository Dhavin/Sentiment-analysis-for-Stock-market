import tweepy
import csv
import sys
import datetime

consumer_key = 'j6pG1V3OYFuFZsazuj1Td0vt2'
consumer_secret = 'CesbfkzRpS7i8ZnaxVNAuDcdnFUy6tpwjYQsgKkHNbrlQaUXAN'
access_token = '1171755115629309953-Abto6o9LwDZB9Jvge38xSOX7rgSPpO'
access_token_secret = 'tA4AwYmGA7b5NmejOZbZ1HkshTEUKAU3pF1eBxwNFfjkI'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

f = input('Enter a Stock : ')

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









from twikit import Client, TooManyRequests
import time
from datetime import datetime
import csv
from configparser import ConfigParser
from random import randint


# how do i convert this to output to sql instead of csv
MINIMUM_TWEETS = 10
QUERY = 'Chris Olave'


def get_tweets(tweets):
        if tweets is None:
            print(f'{datetime.now()} - Getting Tweets...')
            tweets = client.search_tweet(QUERY, product = 'Latest')
        else:
            wait_time = randint(5, 25)
            print(f'{datetime.now()} - Getting Next Tweets after {wait_time} seconds...')
            time.sleep(wait_time)
            tweets = tweets.next()

        return tweets
# login credentials

config = ConfigParser()
config.read('config.ini')
username = config['X']['username']
email = config['X']['email']
password = config['X']['password']

# create a csv file

with open('tweets.csv', 'w', encoding= 'utf-8', newline= '') as file:
    writer = csv.writer(file)
    writer.writerow(['Tweet_Count', 'Username', 'Text', 'Created At', 'ReTweets', 'Likes'])

# authenticate to X.com
#! 1) use the login credentials. 2) use cookies

client = Client(language='en-us') # making it english
# client.login(auth_info_1=username, auth_info_2=email, password=password) # providing the login from config.ini
# client.save_cookies('cookies.json') # saving it as cookies.json so only need to log in one time

client.load_cookies('cookies.json')


tweet_count = 0 
tweets = None

while tweet_count < MINIMUM_TWEETS:

    try:
        tweets = get_tweets(tweets)

    except TooManyRequests as e:
        rate_limit_reset= datetime.fromtimestamp(e.rate_limit_reset)
        print(f'{datetime.now()} Rate Limit reached, waiting until {rate_limit_reset}')
        wait_time = rate_limit_reset - datetime.now()
        time.sleep(wait_time.total_seconds())
        continue

    tweets = get_tweets(tweets)
    
    if tweets is None:
        print(f'{datetime.now()} Getting Tweets') 
        tweets = client.search_tweet(QUERY, product='Top')
    else:
        print(f'{datetime.now()} - Getting Next Tweets...')
        tweets = tweets.next()

    for tweet in tweets:
        tweet_count +=1
        tweet_data = [tweet_count, tweet.user.name, tweet.text, tweet.created_at, tweet.retweet_count, tweet.favorite_count]

# encoding = utf-8 means that you can take emojis into the csv
        with open('tweets.csv', 'a', encoding= 'utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(tweet_data)
    
    print(f'{datetime.now()} - Got {tweet_count} tweets')


print(f'{datetime.now()} - Done Got {tweet_count} tweets found')
import tweepy, requests, re
from textblob import TextBlob
from models import Player, Tweet, Sentiment

def clean_text(text):
    # Removes Special characters, links and mentions from tweet text #
    text = re.sub(r'http\S+' , '', text) # REMOVES URLS
    text = re.sub(r'@\w+','', text) # Removes Mentions
    return text.strip()

def analyze_sentiment(text):
    # Analyze the sentiment of a given tweet in this case :DDDDD 
    analysis = TextBlob(text)
    return analysis.sentiment.polarity 
from django.db import models

# Create your models here.

# models.casecade is when two models are connected via foreign key, it will delete the child object with it.
# Class of a football player
class Player(models.Model):
    name = models.CharField(max_length=100) # Player name
    team = models.CharField(max_length=100) # Team of the player
    position = models.CharField(max_length=20) # Player position        
    
    # Returns the players name when the object is printed or referenced as a string
    def __str__(self):
            return self.name


# Represents a tweet related to a player
# Each tweet is associated with a player, foreignKey relationship
class Tweet(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE) # ForeignKey links each tweet to a player, if player is deleted tweets are deleted too
    
    tweet_id = models.CharField(max_length=255, unique=True) # unique identity for each tweet
    text = models.TextField # Content of the tweet
    created_at = models.DateTimeField() # Time of date creation

    # This method returns the tweet text when the object is printed or referenced as a string
    def __str__(self):
        return self.text


# Sentiment analysis performed on a twee
# Stores the sentiment score (a numeric value) and whether the sentiment is positive, negative or neutral
class Sentiment(models.Model):
     tweet = models.OneToOneField(Tweet, on_delete=models.CASCADE) # Meaning each tweet has one sentiment analysis
    # If tweet is deleted, the sentiment associated with it is also deleted
     score = models.FloatField()  # Range from -1 to 1, negative numbers = negative sentiemtn and positive numbers = positive sentiment
     sentiment = models.CharField(max_length=10)
     
     # This method returns the tweet text and its sentiment when object is printed or referenced as a string
     def __str__(self):
          return f'{self.tweet} - {self.sentiment}'
import tweepy
import json
 
from tweepy import OAuthHandler
 
consumer_key = 'qFrfx5pbJwrL2QxfzvLVufRVi'
consumer_secret = '2Sq6lLxYZhMK2s5N57X5kvVDa8TTGFcgIuqBJpZ9Dufqv0NqWj'
access_token = '3749211929-7efi0f7VxlllNEhpWslKTZqmt3bAqfEpZF0ZQlU'
access_secret = 'OqFqVtS7srb0fuSIGXks9o5qFc8FNi5ScjkKogFLAWILG'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

for status in tweepy.Cursor(api.home_timeline).items(10):
    # Process a single status
    print(status.text)
    

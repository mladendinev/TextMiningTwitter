import time, tweepy, sys
import json
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import pymongo
import os
from time import gmtime, strftime
import datetime


# ## authentication
# username = 'mladenddinev' ## put a valid Twitter username here
# password = 'Wishmeluck123.' ## put a valid Twitter password here
# auth     = tweepy.auth.BasicAuthHandler(username, password)
# api      = tweepy.API(auth)

# def main():
#     track = ['cancer', 'research']

#     listen = SListener(api, 'myprefix')
#     stream = tweepy.Stream(auth, listen)

#     print "Streaming started..."

#     try: 
#         stream.filter(track = track)
#     except:
#         print "error!"
#         stream.disconnect()

# if __name__ == '__main__':
#     main()

consumer_key = "qFrfx5pbJwrL2QxfzvLVufRVi"
consumer_secret = "2Sq6lLxYZhMK2s5N57X5kvVDa8TTGFcgIuqBJpZ9Dufqv0NqWj"
access_token = "3749211929-7efi0f7VxlllNEhpWslKTZqmt3bAqfEpZF0ZQlU"
access_secret = "OqFqVtS7srb0fuSIGXks9o5qFc8FNi5ScjkKogFLAWILG"

auth = OAuthHandler(consumer_key, consumer_secret)  # OAuth object
auth.set_access_token(access_token, access_secret)

listOfKeywords = []

start_time = time.time()



class CustomStreamListener(StreamListener):
    def __init__(self, start_time, time_limit=60):
        self.time = start_time
        self.limit = time_limit
        self.db = pymongo.MongoClient().textMiningStream
        self.counter = 0

    def on_data(self, tweet):
        self.counter= self.counter + 1
        print ("counter", self.counter)
        while (self.counter < 10):
            dataJson = json.loads(tweet)
            self.db['textMiningStream'].insert(dataJson)

    def on_status(self, status):
        print status.text

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True  # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True  # Don't kill the stream


sapi = Stream(auth, CustomStreamListener(start_time))
sapi.filter(track=listOfKeywords)

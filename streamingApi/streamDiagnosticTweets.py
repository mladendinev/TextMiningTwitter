# __author__ = 'mladen'

import time
import sys
import json

from tweepy import Stream
from tweepy.streaming import StreamListener
import pymongo
from textProcessing import textPreprocessing

from auth.Authentication import Authentication
from database import dbOperations as db

filter = ["schizophrenia,schiz", "schizophreniform", "schizo affective", "psychosis", "delusional disorder",
          "shared psychotic", "foile a deux", "induced psychosis", "psychotic disorder"]

start_time = time.time()


class CustomStreamListener(StreamListener):
    def __init__(self):
        # self.time = start_time
        # self.limit = time_limit
        self.db = pymongo.MongoClient().textMiningStream
        self.counter = 0
        self.tweetValidator = textPreprocessing.validators


    def iterationCount(self):
        if db.dbOperations("local").countTweetsInDatabase("streamDiagnostic") == 0:
            numbIter = 1
        else:
            numbIter = db.dbOperations("local").returnLastIteration("streamDiagnostic")
            numbIter += 1
        return numbIter

    def on_data(self, tweet):
        if self.counter == 1000:
            sapi.disconnect()
        self.counter +=1
        print ("counter", self.counter)
        dataJson = json.loads(tweet)

        if self.tweetValidator["Links"](dataJson["text"]) or self.tweetValidator["Retweet"](dataJson["text"]) or not \
                self.tweetValidator["Language"](dataJson["text"]):
            print "Invalid"
            print dataJson["text"]
        else:
            saveDataToJson = {'text': dataJson["text"], "tweet_id": dataJson["id"], 'geo': dataJson["geo"],
                              'coordinates': dataJson["coordinates"], 'place': dataJson["place"],
                              'userId': dataJson["user"]["id"], 'created_at': dataJson["created_at"],
                              'time_zone': dataJson["user"]["time_zone"], "utc_offset": dataJson["user"]["utc_offset"]}
            print "Stored"
            db.dbOperations("local").insertData(saveDataToJson, "streamDiagnostic")

    def on_status(self, status):
        print status.text

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        if (status_code == 420):
            print 'chakai'
            time.sleep(900)
        return True  # Don't kill the stream

    def on_exception(self, exception):
        """Called when an unhandled exception occurs."""
        return exception


    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True  # Don't kill the stream


bum = Authentication()
auth = bum.tweepyAuth()
sapi = Stream(auth, CustomStreamListener())
try:
    sapi.filter(track=filter)
except Exception as e:
    print "Error thrown", e
    sapi.disconnect()

# __author__ = 'mladen'
from tweepy import StreamListener
import json, time, sys
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import os

start_time = time.time()


class listener(StreamListener):
    def __init__(self, start_time, time_limit=60):

        self.time = start_time
        self.limit = time_limit

    def on_data(self, data):

        while (time.time() - self.time) < self.limit:

            try:

                saveFile = open('raw_tweets.json', 'a')
                saveFile.write(data)
                saveFile.write('\n')
                saveFile.close()
                return True

            except BaseException, e:
                print 'failed ondata,', str(e)
                time.sleep(5)
                pass

        exit()

    def on_error(self, status):

        print status

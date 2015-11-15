__author__ = 'mladen'
from auth.Authentication import Authentication
from database import dbOperations
import json
import datetime
import pytz

class ExctractTweetsFromTimeline(object):
    def __init__(self):
        self.count = 100
        self.twitterApiAuth = Authentication().timelineAuth()
        self.twitterApiAuth2 = Authentication().twitterAuth()

    def getTweetsFromTimeline(self,tweet):
        diagnosticTweetId = tweet["tweet_id"]
        userId = tweet["userId"]
        afterDiagnosisTweets = self.twitterApiAuth.user_timeline(user_id = userId,since_id = diagnosticTweetId + 1,count = self.count,
                                                                 exclude_replies = True)


        diagnosticTweet = tweet["text"]
        print diagnosticTweet
        print len(afterDiagnosisTweets)
        beforeDiagCount = 0
        afterDiagCount = 0
        beforeDiagTweets = []
        while beforeDiagCount < 3200:
            tweets = self.twitterApiAuth.user_timeline(user_id = userId, max_id = diagnosticTweetId -1,count=self.count)
            for tweet in tweets:
                beforeDiagTweets.append(tweet["text"])

        while beforeDiagCount < 3200:
            for tweet in afterDiagnosisTweets:
             saveDataToJson = {'text': tweet["text"], "tweet_id": tweet["id"], 'geo': tweet["geo"],
                              'userId': tweet["user"]["id"], 'created_at': tweet["created_at"],
                              'time_zone': tweet["user"]["time_zone"]}


if __name__ == '__main__':
    print "Extracting timeline tweets"
    # tweet = dbOperations.dbOperations().findElementInCollection("diagnosticTweets",{"userId":3399773832})



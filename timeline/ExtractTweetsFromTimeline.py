__author__ = 'mladen'
from auth.Authentication import AuthenticationClass
from DatabaseHelper import dbOperations
import json

class ExctractTweetsFromTimeline(object):
    def __init__(self):
        self.count = 100
        self.twitterApiAuth = AuthenticationClass().timelineAuth()

    def getTweetsFromTimeline(self,tweet):
        diagnosticTweetId = tweet["tweet_id"]
        userId = tweet["userId"]
        afterDiagnosisTweets = self.twitterApiAuth.user_timeline(user_id = userId,since_id = diagnosticTweetId + 1,count = self.count,
                                                                 exclude_replies = True)

        diagnosticTweet = tweet["text"]
        print diagnosticTweet
        print len(afterDiagnosisTweets);
        for tweet in afterDiagnosisTweets:
            saveDataToJson = {'text': tweet["text"], "tweet_id": tweet["id"], 'geo': tweet["geo"],
                              'userId': tweet["user"]["id"], 'created_at': tweet["created_at"],
                              'time_zone': tweet["user"]["time_zone"]}
            dbOperations.dbOperations().insertData(saveDataToJson,"tweetsAfterDiagnosis")


if __name__ == '__main__':
    print "Extracting timeline tweets"
    tweet = dbOperations.dbOperations().findElementInCollection("diagnosticTweets",{"userId":3399773832})
    ExctractTweetsFromTimeline().getTweetsFromTimeline(tweet)



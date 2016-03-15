__author__ = 'mladen'

import sys
import twitter
from auth.Authentication import Authentication
from database import dbOperations
from textProcessing.informationRetrieval import IR
from datetime import timedelta
from textProcessing import textPreprocessing
import tweepy

class ExctractTweetsFromTimeline(object):
    def __init__(self):
        self.count = 100
        self.dbHelper = dbOperations.dbOperations("remote")
        self.twitterApiAuth = Authentication().timelineAuth()
        self.tweetValidator = textPreprocessing.validators

    # def local_time(self, tweet):
    #     if tweet["user"]["utc_offset"] != None:
    #         localtime = IR.calculate_localtime(tweet["created_at"], tweet["user"]["utc_offset"])
    #         dict2 = {"local_time": localtime}
    #         tweetData.update(dict2)
    #     elif tweet["user"]["time_zone"] != None:
    #         localtime = IR.convertTimezoneToLocal(tweet["user"]["time_zone"])
    #         dict2 = {"local_time": localtime}
    #         tweetData = tweetData.update(dict2)
    #     else:
    #         print "No time offset or timezone information in the tweet"

    def saveData(self, tweet, period):
        tweetData = {'text': tweet["text"],
                     "tweet_id": tweet["id"],
                     'geo': tweet["geo"],
                     'userId': tweet["user"]["id"],
                     'created_at': tweet["created_at"],
                     'time_zone': tweet["user"]["time_zone"],
                     "utc_offset": tweet["user"]["utc_offset"],
                     'place': tweet["place"],
                     'coordinates': tweet["coordinates"],
                     'diagnosicTime': period}
        return tweetData

    def findTweetsBeforeDiagnosis(self, diagId, userId, minLimit, maxLimit):
        listIds = []
        beforeDiagCount = 0
        maxIdBefore = diagId - 1
        stop = 0
        while (beforeDiagCount < 5000 and stop == 0):
            try:
                tweets = self.twitterApiAuth.user_timeline(user_id=userId, max_id=maxIdBefore, count=self.count)
                if len(tweets) == 0:
                    print "End of timeline"
                    break
                for tweet in tweets:
                    if (self.tweetValidator["Retweet"](
                            tweet["text"]) or not self.tweetValidator["Language"](tweet["text"])) is False:
                        beforeDiagCount += 1
                        listIds.append(tweet["id"])
                        if minLimit <= IR.format_date(tweet["created_at"]) <= maxLimit:
                            tweetData = self.saveData(tweet, "before")
                            self.dbHelper.insertData(tweetData, "timelineDiagnosedUsers2")
                        else:
                            print "No more tweets to fetch within this range"
                            stop = 1
                            break
                maxIdBefore = min(listIds)
            except twitter.api.TwitterHTTPError as e:
                print e

            except tweepy.error.TweepError as e:
                print e
                break

    def findTweetsAfterDiagnosis(self, diagId, userId, minLimit, maxLimit):
        sinceId = diagId
        listIds = []
        afterDiagCount = 0
        stop = 0
        while (afterDiagCount < 5000 and stop == 0):
            try:
                tweets = self.twitterApiAuth.user_timeline(user_id=userId, since_id=sinceId, count=self.count)
                if len(tweets) == 0:
                    print "End of timeline"
                    break

                for tweet in tweets:
                    afterDiagCount += 1
                    listIds.append(tweet["id"])
                    if (self.tweetValidator["Retweet"](
                            tweet["text"]) or not self.tweetValidator["Language"](tweet["text"])) is False:
                        if minLimit <= IR.format_date(tweet["created_at"]) <= maxLimit:
                            tweetData = self.saveData(tweet, "after")
                            self.dbHelper.insertData(tweetData, "timelineDiagnosedUsers2")
                        else:
                            print "No more tweets to fetch within this range"
                            stop = 1
                            break
                    sinceId = max(listIds)
            except twitter.api.TwitterHTTPError as e:
                print e

            except tweepy.error.TweepError as e:
                print e
                break

    def getTweetsFromTimeline(self, tweet):
        diagnosticTweetId = tweet["tweet_id"]
        seen = []
        if diagnosticTweetId not in seen:
            seen.append(diagnosticTweetId)
            userId = tweet["userId"]
            diagnosticDate = tweet["created_at"]
            formatDiagnosticDate = IR.format_date(diagnosticDate)

            timeframeBefore = timedelta(days=48)
            timeframeAfter = timedelta(days=1000)
            maxLimit = formatDiagnosticDate + timeframeAfter
            minLimit = formatDiagnosticDate - timeframeBefore
            print "Tweets before the diagnosis"
            self.findTweetsBeforeDiagnosis(diagnosticTweetId, userId, minLimit, formatDiagnosticDate)
            print "Tweets afrer the diagnosis"
            self.findTweetsAfterDiagnosis(diagnosticTweetId, userId, formatDiagnosticDate, maxLimit)


if __name__ == '__main__':
    print "Extracting timeline tweets"
    try:
        rohanDiagnostic = dbOperations.dbOperations("remote").returnDocsForTimelineExt('diagnosticTweets',
                                                                                       "user.rmorris.label",
                                                                                       'positve')
        natalieDiagnostic = dbOperations.dbOperations("remote").returnDocsForTimelineExt('diagnosticTweets',
                                                                                         "user.nberry.label",
                                                                                         'positve')
        # extraSet = dbOperations.dbOperations("remote").returnDocsForTimelineExt('diagnosticTweets',
        #                                                                                  "user.extra.label",
        #                                                                                  'positve')
        seen = []
        allDiagnostic = natalieDiagnostic + natalieDiagnostic
        if len(allDiagnostic) == 0:
            print "No new diagnostic Tweets"
        else:
            for tweet in allDiagnostic:
                if tweet['tweet_id'] not in seen:
                    seen.append(tweet['tweet_id'])
                    ExctractTweetsFromTimeline().getTweetsFromTimeline(tweet)
                    dbOperations.dbOperations("remote").updateDocumnet("diagnosticTweets", {"_id": tweet['_id']},
                                                                       {'$set': {'processedTimeline': "yes"}})
    except twitter.api.TwitterHTTPError as e:
        print e

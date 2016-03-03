__author__ = 'mladen'

import sys

from auth.Authentication import Authentication
from database import dbOperations
from textProcessing.informationRetrieval import IR
from datetime import timedelta


class ExctractTweetsFromTimeline(object):
    def __init__(self):
        self.count = 100
        self.dbHelper = dbOperations.dbOperations("remote")
        self.twitterApiAuth = Authentication().timelineAuth()

    def findTweetsBeforeDiagnosis(self, diagId, userId, minLimit, maxLimit):
        listIds = []
        beforeDiagCount = 0
        maxIdBefore = diagId - 1
        stop = 0

        while beforeDiagCount < 3200:
            tweets = self.twitterApiAuth.user_timeline(user_id=userId, max_id=maxIdBefore, count=self.count)
            if len(tweets) == 0:
                print "End of timeline"
                break
            if stop == 0:
                for tweet in tweets:
                    beforeDiagCount += 1
                    listIds.append(tweet["id"])
                    if minLimit <= IR.format_date(tweet["created_at"]) <= maxLimit:
                        tweetData = {'text': tweet["text"],
                                     "tweet_id": tweet["id"],
                                     'geo': tweet["geo"],
                                     'userId': tweet["user"]["id"],
                                     'created_at': tweet["created_at"],
                                     'time_zone': tweet["user"]["time_zone"],
                                     "utc_offset": tweet["user"]["utc_offset"],
                                     'place': tweet["place"],
                                     'coordinates': tweet["coordinates"],
                                     'diagnosicTime': "before"}
                        if tweet["user"]["utc_offset"] != None:
                            localtime = IR.calculate_localtime(tweet["created_at"], tweet["user"]["utc_offset"])
                            dict2 = {"local_time": localtime}
                            tweetData.update(dict2)
                        elif tweet["user"]["time_zone"] != None:
                            localtime = IR.convertTimezoneToLocal(tweet["user"]["time_zone"])
                            dict2 = {"local_time": localtime}
                            tweetData = tweetData.update(dict2)
                        else:
                            print "No time offset or timezone information in the tweet"

                        self.dbHelper.insertData(tweetData, "timelineDiagnosedUsers")
                    else:
                        print "No more tweets to fetch within this range"
                        stop = 1
                        break
                maxIdBefore = min(listIds)
            else:
                break

    def findTweetsAfterDiagnosis(self, diagId, userId, minLimit, maxLimit):
        sinceId = diagId
        listIds = []
        afterDiagCount = 0
        stop = 0
        while afterDiagCount < 3200:
            tweets = self.twitterApiAuth.user_timeline(user_id=userId, since_id=sinceId, count=self.count)
            if len(tweets) == 0:
                print "End of timeline"
                break
            if stop == 0:
                for tweet in tweets:
                    afterDiagCount += 1
                    listIds.append(tweet["id"])
                    if minLimit <= IR.format_date(tweet["created_at"]) <= maxLimit:
                        tweetData = {'text': tweet["text"],
                                     "tweet_id": tweet["id"],
                                     'geo': tweet["geo"],
                                     'userId': tweet["user"]["id"],
                                     'created_at': tweet["created_at"],
                                     'time_zone': tweet["user"]["time_zone"],
                                     "utc_offset": tweet["user"]["utc_offset"],
                                     'place': tweet["place"],
                                     'coordinates': tweet["coordinates"],
                                     'diagnosicTime': "after"}
                        if tweet["user"]["utc_offset"] != None:
                            print tweet["user"]["utc_offset"]
                            print tweet["text"]
                            localtime = IR.calculate_localtime(tweet["created_at"], tweet["user"]["utc_offset"])
                            dict2 = {"local_time": localtime}
                            tweetData.update(dict2)
                        elif tweet["user"]["time_zone"] != None:
                            localtime = IR.convertTimezoneToLocal(tweet["user"]["time_zone"])
                            dict2 = {"local_time": localtime}
                            tweetData = tweetData.update(dict2)
                        else:
                            print "No time offset or timezone information in the tweet"

                        # Store data to database
                        self.dbHelper.insertData(tweetData, "timelineDiagnosedUsers")
                    else:
                        print "No more tweets to fetch within this range"
                        stop = 1
                        break
                sinceId = max(listIds)
            else:
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
        extraSet = dbOperations.dbOperations("remote").returnDocsForTimelineExt('diagnosticTweets',
                                                                                         "user.extra.label",
                                                                                         'positve')

        allDiagnostic = natalieDiagnostic + natalieDiagnostic + extraSet
        if len(allDiagnostic) == 0:
            print "No new diagnostic Tweets"
        else:
            for tweet in allDiagnostic:
                ExctractTweetsFromTimeline().getTweetsFromTimeline(tweet)
                dbOperations.dbOperations("remote").updateDocumnet("diagnosticTweets", {"_id": tweet['_id']},
                                                                   {'$set': {'processedTimeline': "yes"}})
    except Exception as e:
        print e
        sys.exit(0)


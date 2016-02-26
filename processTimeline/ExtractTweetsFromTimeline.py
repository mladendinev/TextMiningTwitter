__author__ = 'mladen'
from datetime import datetime
from datetime import timedelta

from auth.Authentication import Authentication
from database import dbOperations
import pytz


class ExctractTweetsFromTimeline(object):
    def __init__(self):
        self.count = 100
        self.dbHelper = dbOperations.dbOperations("remote")
        self.twitterApiAuth = Authentication().timelineAuth()

    def format_date(self, date):
        format = datetime.strptime(date, '%a %b %d %H:%M:%S '
                                         '+0000 %Y')
        return format

    def convertTimezoneToLocal(self, timezoneTweet):
        localTime = pytz.timezone(timezoneTweet)
        return localTime

    def calculate_localtime(self, date, offset):
        date = self.format_date(date)
        offset /= 3600
        localtime = date + timedelta(hours=offset)
        return localtime

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
                    if minLimit <= self.format_date(tweet["created_at"]) <= maxLimit:
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
                            localtime = self.calculate_localtime(tweet["created_at"], tweet["user"]["utc_offset"])
                            dict2 = {"local_time": localtime}
                            tweetData.update(dict2)
                        elif tweet["user"]["time_zone"] != None:
                            localtime = self.convertTimezoneToLocal(tweet["user"]["time_zone"])
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
                    if minLimit <= self.format_date(tweet["created_at"]) <= maxLimit:
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
                            print tweet["user"]["utc_offset"]
                            print tweet["text"]
                            localtime = self.calculate_localtime(tweet["created_at"], tweet["user"]["utc_offset"])
                            dict2 = {"local_time": localtime}
                            tweetData.update(dict2)
                        elif tweet["user"]["time_zone"] != None:
                            localtime = self.convertTimezoneToLocal(tweet["user"]["time_zone"])
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
        userId = tweet["userId"]
        diagnosticDate = tweet["created_at"]
        formatDiagnosticDate = self.format_date(diagnosticDate)

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
    # tweet = dbOperations.dbOperations("local").findElementInCollection("diagnosticTweets", {"tweet_id": 658906748997255169})
    rohanDiagnostic = dbOperations.dbOperations("remote").returnDocsWithSpecificField('diagnosticTweets', "user.rmorris.label",
                                                                                      'positive')
    natalieDiagnostic = dbOperations.dbOperations("remote").returnDocsWithSpecificField('diagnosticTweets', "user.nberry.label",
                                                                                       'positive')
    allDiagnostic = natalieDiagnostic +natalieDiagnostic
    for tweet in allDiagnostic:
        ExctractTweetsFromTimeline().getTweetsFromTimeline(tweet)

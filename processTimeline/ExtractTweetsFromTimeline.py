__author__ = 'mladen'
from datetime import datetime
from datetime import timedelta

from auth.Authentication import Authentication
from database import dbOperations


class ExctractTweetsFromTimeline(object):
    def __init__(self):
        self.count = 100
        self.twitterApiAuth = Authentication().timelineAuth()

    def format_date(self, date):
        format = datetime.strptime(date, '%a %b %d %H:%M:%S '
                                         '+0000 %Y')
        return format

    def calculate_localtime(self, date, offset):
        date = self.format_date(date)
        offset /= 3600
        localtime = date + timedelta(hours=offset)
        return localtime

    def findTweetsBeforeDiagnosis(self, diagId, userId, minLimit, maxLimit):
        listIds = []
        beforeDiagCount = 0
        maxIdBefore = diagId - 1
        while beforeDiagCount < 3200:
            tweets = self.twitterApiAuth.user_timeline(user_id=userId, max_id=maxIdBefore, count=self.count)
            print len(tweets)
            if len(tweets) == 0:
                print "End of timeline"
                break

            for tweet in tweets:
                beforeDiagCount += 1
                listIds.append(tweet["id"])
                if minLimit <= self.format_date(tweet["created_at"]) <= maxLimit:
                    print tweet["text"]
                    print tweet["created_at"]
                else:
                   print "No more tweets to fetch within this range"
                   break
            maxIdBefore = min(listIds)

    def findTweetsAfterDiagnosis(self, diagId, userId, minLimit, maxLimit):
        sinceId = diagId
        listIds = []
        afterDiagCount = 0
        while afterDiagCount < 3200:
            tweets = self.twitterApiAuth.user_timeline(user_id=userId, since_id=sinceId, count=self.count)
            if len(tweets) == 0:
                print "End of timeline"
                break

            for tweet in tweets:
                afterDiagCount += 1
                listIds.append(tweet["id"])
                if minLimit <= self.format_date(tweet["created_at"]) <= maxLimit:
                    print tweet["text"]
                    print tweet["created_at"]
                else:
                   print "opii"
            sinceId = max(listIds)

    def getTweetsFromTimeline(self, tweet):
        diagnosticTweetId = tweet["tweet_id"]
        userId = tweet["userId"]
        diagnosticDate = tweet["created_at"]
        diagnosticTweet = tweet["text"]
        timeOffSet = tweet["utc_offset"]
        diagnosticDate = self.format_date(diagnosticDate)

        timeframe = timedelta(days=48)
        maxLimit = diagnosticDate + timeframe
        minLimit = diagnosticDate - timeframe
        self.findTweetsBeforeDiagnosis(diagnosticTweetId, userId, minLimit, maxLimit)


if __name__ == '__main__':
    print "Extracting timeline tweets"
    tweet = dbOperations.dbOperations().findElementInCollection("diagnosticTweets", {"userId": 267877188})
    ExctractTweetsFromTimeline().getTweetsFromTimeline(tweet)

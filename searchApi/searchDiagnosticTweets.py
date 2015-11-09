# __author__ = 'mladen'

from auth.Authentication import AuthenticationClass
from tweetsHelper import tweetsOperations
import time
from database import dbOperations
import os
from celery import Celery
import sys
import logging
import twitter
count = 10
twitterApiAuth = AuthenticationClass().twitterAuth()
disorderListFile = "/home/mladen/FinalYearProject/word_lists/disorder_list.txt"
wordDictionary = tweetsOperations.getSearchTermsFromFile(disorderListFile)

app = Celery('tasks')
app.config_from_object('celeryconfig')


@app.task
def requestNewDiagnosticTweets(query, sinceId, maxId):
    try:
        if (maxId != 0):
            print sinceId, maxId, count, query
            tweets = twitterApiAuth.search.tweets(q=query, max_id= maxId - 1,since_id = sinceId)
            return tweets
        else:
            print sinceId, maxId, count, query
            tweets = twitterApiAuth.search.tweets(q=query, count=count,since_id=sinceId)
            return tweets

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno, e)

@app.task
def fetchDiagnosticTweets():
    logging.info("Fetch tweets")
    tweetsReceived = []
    tweetValidator = tweetsOperations.validators
    dbHelper = dbOperations

    if dbHelper.dbOperations().countTweetsInDatabase("diagnosticTweets") == 0:
        numbIter = 1
    else:
        numbIter = dbOperations.dbOperations().returnLastIteration("diagnosticTweets")
        numbIter = numbIter + 1

    for keyword in wordDictionary:
        print keyword
        countTweets = 0
        maxId = 0
        sinceId = 0
        listIds = []
        numbValidTweets = 0
        print "Loop starts", maxId
        text = keyword.rstrip('\n')
        while countTweets < 100:
            try:
                print ("Number of tweets"), countTweets
                # _sinceId = tweetsOperations.getSinceId("diagnosticTweets")

                print text
                sinceId = dbOperations.dbOperations().findElementInCollection("queries", {"query": text})["since_id"]
                print "sinceID", sinceId
                print "maxId", maxId
                tweets = twitterApiAuth.search.tweets(q=text,count= count, max_id= maxId, since_id = sinceId)
                time.sleep(3)
                print len(tweets)   
                if len(tweets["statuses"]) == 0:
                    print 'no new tweets'
                    break

                for tweet in tweets['statuses']:
                    countTweets +=1
                    listIds.append(int(tweet["id"]))
                    searchTweet = {"tweet_id": long(str(tweet["id"]))}
                    if dbOperations.dbOperations().findElementInCollection("sleepTweets", searchTweet) == None:
                        if tweetValidator["Links"](tweet["text"]) or tweetValidator["Retweet"](tweet["text"]) or not \
                                tweetValidator["Language"](tweet["text"]):
                            print "invalid"
                        else:

                            # if tweetDiseaseChecker.findIfDiagnosticFetch(tweet["text"],
                            #                                              keyword) or tweetDiseaseChecker.findIfContainsMed(
                            #         tweet["text"], keyword):
                            saveDataToJson = {'text': tweet["text"], "tweet_id": tweet["id"], 'geo': tweet["geo"],
                                              'iteration': numbIter,
                                              'userId': tweet["user"]["id"], 'created_at': tweet["created_at"],
                                              'time_zone': tweet["user"]["time_zone"]}
                            dbOperations.dbOperations().insertData(saveDataToJson, "diagnosticTweets")
                            numbValidTweets += 1
                            print "Stored valid tweet"

                maxId = min(listIds)
                sinceId = max(listIds)
                print "Update since id", sinceId
                dbOperations.dbOperations().updateDocumnet("queries", {"query": text}, {'$set': {'since_id': long(sinceId)}})
            except twitter.api.TwitterHTTPError as e:
                print "twitter.api.TwitterHTTPError"
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                break
            # except tw as e:

                #
                # datapath = '/home/mladen/FinalYearProject/data/statistics'
                # completeName = os.path.join(datapath, 'diagnosisStats' + str(numbIter) + ".txt")
                # f = open(completeName, 'w')
                # f.write("Number of tweets fetched" + " " + str(self._countTweets))
                # f.write('\n')
                # f.write("Number of valid tweets" + " " + str(self._numbValidTweets))


if __name__ == '__main__':
    print "Searching tweets..."
    fetchDiagnosticTweets()
# __author__ = 'mladen'
import time
import os
import sys
import logging
import logging.config

from celery import Celery
import twitter

from auth.Authentication import Authentication
from tweetsHelper import tweetsOperations
from database import dbOperations

count = 30
twitterApiAuth = Authentication().twitterAuth()
disorderListFile = "/home/mladen/TextMiningTwitter/word_lists/disorder_list.txt"
wordDictionary = tweetsOperations.getSearchTermsFromFile(disorderListFile)

app = Celery('tasks')
app.config_from_object('celeryconfig')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@app.task
def requestNewDiagnosticTweets(query, count, sinceId, maxId):
    try:
        if (maxId != 0):
            tweets = twitterApiAuth.search.tweets(q=query, count=count, max_id=maxId,since_id = sinceId)
            time.sleep(3)
            return tweets
        else:
            tweets = twitterApiAuth.search.tweets(q=query, count=count, since_id=sinceId)
            return tweets

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno, e)


@app.task
def fetchDiagnosticTweets():
    logger.info("Fetching tweets")
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
        print "Loop starts"
        text = keyword.rstrip('\n')
        while countTweets < 120:
            try:
                print ("Number of tweets"), countTweets
                sinceId = dbOperations.dbOperations().findElementInCollection("queries", {"query": text})["since_id"]
                tweets = requestNewDiagnosticTweets(text, count, sinceId, maxId)
                time.sleep(1)
                # print len(tweets)
                if len(tweets["statuses"]) == 0:
                    if (len(listIds) == 0):
                        print "No new tweets since last time"
                        break
                    else:
                        sinceId = max(listIds)
                        print "Update since id", sinceId
                        dbOperations.dbOperations().updateDocumnet("queries", {"query": text},
                                                           {'$set': {'since_id': long(sinceId)}})
                        print 'Reached end of stack'
                        break

                for tweet in tweets['statuses']:
                    print tweet["id"]
                    countTweets += 1
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
                            saveDataToJson = {'text': tweet["text"] , "tweet_id": tweet["id"], 'geo': tweet["geo"],
                                              'iteration': numbIter,
                                              'userId': tweet["user"]["id"], 'created_at': tweet["created_at"],
                                              'time_zone': tweet["user"]["time_zone"], "utc_offset":tweet["user"]["utc_offset"],
                                              'place': tweet["place"],
                                              'coordinates': tweet["coordinates"]}
                            dbOperations.dbOperations().insertData(saveDataToJson, "diagnosticTweets")
                            numbValidTweets += 1
                            print "Stored valid tweet"
                maxId = min(listIds) -1

            except twitter.api.TwitterHTTPError as e:
                logger.error("Exception thrown %e",exc_info=True)

                # except tw as e:

                #
                # datapath = '/home/mladen/TextMiningTwitter/data/statistics'
                # completeName = os.path.join(datapath, 'diagnosisStats' + str(numbIter) + ".txt")
                # f = open(completeName, 'w')
                # f.write("Number of tweets fetched" + " " + str(self._countTweets))
                # f.write('\n')
                # f.write("Number of valid tweets" + " " + str(self._numbValidTweets))


if __name__ == '__main__':
    print "Searching tweets..."
    fh = logging.FileHandler('/home/mladen/TextMiningTwitter/auth/log/logDiagnostic.log')
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    fetchDiagnosticTweets()


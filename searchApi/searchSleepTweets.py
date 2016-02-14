# __author__ = 'mladen'
import time
import os
import logging
import logging.config
from celery import Celery

from database import dbOperations
from textProcessing import textPreprocessing
from auth.Authentication import Authentication
import sys
import twitter
from textProcessing import textExtractor

app = Celery('tasks')
app.config_from_object('celeryconfig')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

sleepPhrases = "/home/mladen/TextMiningTwitter/word_lists/sleepRelatedKeywords.txt"
wordDictionary = textExtractor.getTerms(sleepPhrases)

count = 5
twitterApiAuth = Authentication().twitterAuth()  # auth credentials


@app.task
def requestNewSleepTweets(query, count, sinceId, maxId):
    try:
        if (maxId != 0):
            tweets = twitterApiAuth.search.tweets(q=query, count=count, max_id=maxId, since_id=sinceId)
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
def fetchSleepRealtedTweets():
    for keyword in wordDictionary:
        print "Searching for" + keyword + "starts"
        print keyword
        count = 0
        maxId = 0
        listIds = []
        numbValidTweets = 0
        sinceId = 0
        # query1 = "insomnia OR sleep issues OR wish i could sleep"
        # query2 = 'sleeping pills OR sleeping'
        tweetValidator = textPreprocessing.validators
        global numbIter
        dbHelper = dbOperations.dbOperations("local")

        numbIter = dbHelper.returnFieldIteration("sleepTweetsTest", keyword, "iteration")

        if numbIter == None:
            numbIter = 1
        else:
            print "Iteration {} for the key phrase {}".format(numbIter, keyword)
            numbIter = numbIter + 1

        while (count <= 15):
            try:
                print ("counter", count)
                sinceId = dbHelper.findElementInCollection("sleepQueries", {"query": keyword})["since_id"]
                tweets = requestNewSleepTweets(keyword, count, maxId, sinceId)

                if len(tweets["statuses"]) == 0:
                    if (len(listIds) == 0):
                        print "No new tweets since last time"
                        break
                    else:
                        sinceId = max(listIds)
                        print "Update since id", sinceId
                        dbHelper.updateDocumnet("sleepQueries", {"query": keyword},
                                                {'$set': {'since_id': long(sinceId)}})
                        print 'Reached end of stack'
                        break

                for tweet in tweets["statuses"]:
                    listIds.append(int(tweet["id"]))
                    count += 1
                    if dbHelper.findElementInCollection("sleepTweets", {"userId": tweet["id"]}) == None:
                        if tweetValidator["Links"](tweet["text"]) or tweetValidator["Retweet"](tweet["text"]) or not \
                                tweetValidator["Language"](tweet["text"]):
                            print "Invalid Tweet"
                        else:
                            saveDataToJson = {'text': tweet["text"],
                                              "tweet_id": tweet["id"],
                                              'geo': tweet["geo"],
                                              'iteration': numbIter,
                                              'userId': tweet["user"]["id"],
                                              'created_at': tweet["created_at"],
                                              'time_zone': tweet["user"]["time_zone"],
                                              "utc_offset": tweet["user"]["utc_offset"],
                                              'place': tweet["place"],
                                              'coordinates': tweet["coordinates"],
                                              'search_terms': keyword}
                            dbHelper.insertData(saveDataToJson, "sleepTweetsTest")
                            numbValidTweets += 1
                            print "Stored valid tweet"

                maxId = min(listIds) - 1
                if count >= 15:
                    print "I have to update the since id, limit exceeded"
                    print 'Count', count
                    sinceId = max(listIds)
                    dbHelper.updateDocumnet("sleepQueries", {"query": keyword},
                                            {'$set': {'since_id': long(sinceId)}})

            except twitter.api.TwitterHTTPError as e:
                logger.error("Exception thrown %e", exc_info=True)


if __name__ == '__main__':
    print "Searching tweets..."
    fh = logging.FileHandler('/home/mladen/TextMiningTwitter/auth/log/logDiagnostic.log')
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    fetchSleepRealtedTweets()


# datapath = '/home/mladen/TextMiningTwitter/data'
# completeName = os.path.join(datapath, 'statistics' + str(numbIter) + ".txt")
# f = open(completeName, 'w')
# f.write("Number of tweets fetched" + " " + str(count))
# f.write('\n')
# f.write("Number of valid tweets" + " " + str(numbValidTweets))
#
# if __name__ == '__main__':
#     print "Searching tweets..."
#     runTweets()

# print json.dumps(statuses[0], indent=1)

# print 'Length: %s' % len(statuses)

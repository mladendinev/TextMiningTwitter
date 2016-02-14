import tweepy
import json
from tweepy.parsers import JSONParser
import os
import sys
from textProcessing import textPreprocessing
import time
from database import dbOperations

from tweepy import OAuthHandler

consumer_key = 'PJMh06lg3UgkIRVM0sdT8NDgP'
consumer_secret = 'ocGPOr0pVclzfZZO0K0ZexBJ6w6Jf7QjNZ08EPcRWqiyhGwBCp'
access_token = '3749211929-7efi0f7VxlllNEhpWslKTZqmt3bAqfEpZF0ZQlU'
access_secret = 'OqFqVtS7srb0fuSIGXks9o5qFc8FNi5ScjkKogFLAWILG'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
#
# result =  tweepy.Cursor(api.search,q='Disases',count=10, result_type='mixed').items(10)
disorderListFile = "/home/mladen/TextMiningTwitter/word_lists/disorder_list.txt"
wordDictionary = textPreprocessing.getSearchTermsFromFile(disorderListFile)



#
# for res in results1["statuses"]:
#     kurec = json.dumps(res, indent=1)
#     print res["user"]["time_zone"]
#
#     datapath = '/home/mladen/TextMiningTwitter/data'
#     completeName = os.path.join(datapath, 'kur1'+ ".txt")
#     f = open(completeName, 'w')
#     f.write(kurec)
#     f.write('\n')
#     break
count = 50

# @app.task
# def requestNewTweets(query, maxId, sinceId):
#     # tweets = twitterApiAuth.search.tweets(q=query, count=count, result_type='mixed',max_id = maxId, since_id = sinceId)
#
#     return tweets


def requestNewDiagnosticTweets(query, sinceId, maxId):
    try:
        # if (maxId != 0):

        print sinceId, maxId, count, query
        max = long(maxId)
        # tweets = twitterApiAuth.search.tweets(q=query,count = count, max_id= maxId - 1)
        results1 = api.search(q=query, count=count, max_id=max, since_id=sinceId)
        # else:
        #     # print sinceId, maxId, count, query
        #     results1 = api.search(q=query, count=count,result_type='mixed', since_id = sinceId)
        return results1

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno, e)


def fetchDiagnosticTweets():
    tweetValidator = textPreprocessing.validators
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
        while countTweets < 300:
            try:
                print ("Number of tweets"), countTweets
                # _sinceId = tweetsOperations.getSinceId("diagnosticTweets")

                print text
                sinceId = dbOperations.dbOperations().findElementInCollection("queries", {"query": text})["since_id"]
                print "sinceID", sinceId

                tweets = api.search(q=text, count=count, max_id=663686607401275392, since_id=663688897143025664)

                time.sleep(3)
                print len(tweets)
                if len(tweets["statuses"]) == 0:
                    print 'no new tweets'
                    break

                for tweet in tweets['statuses']:
                    print tweet["id"]
            # countTweets += len(tweets['statuses'])
            #         listIds.append(long(tweet["id"]))
            #         searchTweet = {"tweet_id": long(str(tweet["id"]))}
            #         if dbOperations.dbOperations().findElementInCollection("sleepTweets", searchTweet) == None:
            #             if tweetValidator["Links"](tweet["text"]) or tweetValidator["Retweet"](tweet["text"]) or not \
            #                     tweetValidator["Language"](tweet["text"]):
            #                 print "invalid"
            #             else:
            #
            #                 # if tweetDiseaseChecker.findIfDiagnosticFetch(tweet["text"],
            #                 #                                              keyword) or tweetDiseaseChecker.findIfContainsMed(
            #                 #         tweet["text"], keyword):
            #                 saveDataToJson = {'text': tweet["text"], "tweet_id": long(tweet["id"]), 'geo': tweet["geo"],
            #                                   'iteration': numbIter,
            #                                   'userId': tweet["user"]["id"], 'created_at': tweet["created_at"],
            #                                   'time_zone': tweet["user"]["time_zone"]}
            #                 dbOperations.dbOperations().insertData(saveDataToJson, "diagnosticTweets")
            #                 time.sleep(1)
            #                 numbValidTweets += 1
            #                 print "Stored valid tweet"
            #
            #     maxId = min(listIds)
            #     sinceId = max(listIds)
            #     print "Update since id", sinceId
            #     dbOperations.dbOperations().updateDocumnet("queries", {"query": text}, {'$set': {'since_id': long(sinceId)}})
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno, e)


if __name__ == '__main__':
    print "Searching tweets..."
    fetchDiagnosticTweets()

# __author__ = 'mladen'
import time
import os

from celery import Celery

from database import dbOperations
from tweetsHelper import tweetsOperations
from auth.Authentication import Authentication



# # statuses = search_results['statuses']
#
# for _ in range(5):
#     print "Length  of statuses", len(statuses)
#     try:
#         next_results = search_results['search_metadata']['next_results']
#     except KeyError, e:
#         break
#
#         kwargs = dict([kv.split('=') for kv in next_results[1:].split("&")])
#         search_results = twitter_api.search.tweets(**kwargs)
#         statuses += search_results['statuses']

app = Celery('tasks')
app.config_from_object('celeryconfig')

count = 10
twitterApiAuth = Authentication().twitterAuth()  # auth credentials


@app.task
def add(x, y):
    print "executing"
    return x + y

@app.task
def requestNewTweets(query, maxId, sinceId):
    tweets = twitterApiAuth.search.tweets(q=query, count=count, result_type='mixed',max_id = maxId, since_id = sinceId)
    return tweets

# 660940574858416128

# 660942288437121024
@app.task
def runTweets():
    count = 0
    maxId = 0
    tweetsReceived = []
    read = True
    numbValidTweets = 0
    query1 = "insomnia OR sleep issues OR wish i could sleep"
    query2 = 'sleeping pills OR sleeping'
    tweetValidator = tweetsOperations.validators
    global numbIter
    dbHelper = dbOperations

    if dbHelper.dbOperations().countTweetsInDatabase("sleepTweets") == 0:
        numbIter = 1
    else:
        numbIter = dbOperations.dbOperations().returnLastIteration("sleepTweets")
        numbIter = numbIter + 1

    while (count < 200):
        listIds = []
        print ("counter", count)
        try:
            if read == True:
                sinceId = dbOperations.dbOperations().findElementInCollection("queries",{"id": 1})["since_id"]
                tweets = requestNewTweets(query1,maxId,sinceId)
                read = False
                time.sleep(3)

            else:
                sinceId = dbOperations.dbOperations().findElementInCollection("queries",{"id": 2})["since_id"]
                print sinceId
                tweets =requestNewTweets(query2,maxId,sinceId)
                read = True
                time.sleep(3)

            for items in tweets["statuses"]:
                print items["user"]["id"]
                listIds.append(items["id"])
                count += 1
                searchTweet = {"tweet_id" : long(str(items["id"]))}
                if dbOperations.dbOperations().findElementInCollection("sleepTweets",searchTweet) == None:
                    print "New element found"

                    tweetsReceived.append(items["text"])
                    dataJson = {'text': items["text"], "tweet_id": items["id"], 'geo': items["geo"], 'iteration': numbIter,
                            'userId': items["user"]["id"]}

                    if tweetValidator["Links"](items["text"]) or tweetValidator["Retweet"](items["text"]) or not \
                      tweetValidator["Language"](items["text"]):
                    # print "Invalid Tweets"
                         pass
                    else:
                         print "Valid tweet"
                         dbOperations.dbOperations().insertData(dataJson, "sleepTweets")
                         numbValidTweets += 1

            maxId = min(listIds) - 1
            sinceId = max(listIds)
            if read:
                dbOperations.dbOperations().updateDocumnet("queries",{"id": 1}, {'$set': {'since_id': sinceId}})
            else:
                dbOperations.dbOperations().updateDocumnet("queries",{"id": 2}, {'$set': {'since_id': sinceId}})


        except Exception as e:
            print ("Exception searching tweets", e)
            break

        datapath = '/home/mladen/FinalYearProject/data'
        completeName = os.path.join(datapath, 'statistics' + str(numbIter) + ".txt")
        f = open(completeName, 'w')
        f.write("Number of tweets fetched" + " " + str(count))
        f.write('\n')
        f.write("Number of valid tweets" + " " + str(numbValidTweets))



if __name__ == '__main__':
    print "Searching tweets..."
    runTweets()

# print json.dumps(statuses[0], indent=1)

# print 'Length: %s' % len(statuses)

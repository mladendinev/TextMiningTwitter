__author__ = 'mladen'
from multiprocessing import Pool, Manager

import requests
from database.dbOperations import dbOperations as db


def main():
    sleepTweets = db("remote").returnDocsWithSpecificField("timelineDiagnosedUsers2")

    collection = []
    # for i in range(0, 10):
    #     tweet = db.find().limit(-1).skip(random.randint(0, db.count() - 1)).next()
    #     collection += [tweet]

    for tweet in sleepTweets:
        collection += [tweet]

    enriched_tweets = enrich(collection)
    # # Store data in MongoDB
    store(enriched_tweets)

    return


def enrich(tweets):
    pool = Pool(processes=10)
    mgr = Manager()
    result_queue = mgr.Queue()
    for tweet in tweets:
        pool.apply_async(get_text_sentiment, (tweet, result_queue))

    pool.close()
    pool.join()
    collection = []
    while not result_queue.empty():
        collection += [result_queue.get()]

    print "Enrichment complete! Enriched %d Tweets" % len(collection)
    return collection


def get_text_sentiment(tweet, output):
    nltk_sentiment_url = "http://text-processing.com/api/sentiment/"

    # Parameter list, containing the data to be enriched
    # print tweet['text']
    parameters = {
        'text': tweet['text']
    }

    try:
        results = requests.post(url=nltk_sentiment_url, data=parameters)
        # print results.text
        response = results.json()

    except Exception as e:
        print "Error while calling TextGetTargetedSentiment on Tweet (ID %s)" % tweet['id']
        print "Error:", e
        return

    try:

        tweet['sentiment'] = response['label']
        tweet['score'] = response['probability'][response['label']]
        tweet['score'] = 0.

        if tweet['sentiment'] in ('pos', 'neg', 'neutral'):
            tweet['score'] = response['probability'][response['label']]
        output.put(tweet)

    except Exception as e:
        print "Error:", e
        print "Request:", results.url
        print "Response:", response
    return


def store(tweets):
    for tweet in tweets:
        db("remote").updateDocumnet('timelineDiagnosedUsers2', {"_id": tweet['_id']},
                                    {"$set": {"sentiment": tweet["sentiment"]}})



if __name__ == "__main__":
    main()

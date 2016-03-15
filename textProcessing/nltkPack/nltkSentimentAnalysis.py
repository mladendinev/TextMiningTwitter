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

    # # Print some interesting results to the screen
    # print_results()
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
        # data = json.dumps(results.text)
        # print data
        # print type(results)

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
        print "D'oh! There was an error enriching Tweet (ID %s)" % tweet['id']
        print "Error:", e
        print "Request:", results.url
        print "Response:", response

    return


def store(tweets):
    for tweet in tweets:
        db("remote").updateDocumnet('timelineDiagnosedUsers2', {"_id": tweet['_id']}, {"$set": {"sentiment": tweet["sentiment"]}})

def print_results():
    print ''
    print ''
    print '###############'
    print '#    Stats    #'
    print '###############'
    print ''
    print ''

    # tweets = databaseInstance()
    #
    # num_positive_tweets = tweets.find({"sentiment": "pos"}).count()
    # num_negative_tweets = tweets.find({"sentiment": "neg"}).count()
    # num_neutral_tweets = tweets.find({"sentiment": "neutral"}).count()
    # num_tweets = tweets.find().count()
    #
    # if num_tweets != sum((num_positive_tweets, num_negative_tweets, num_neutral_tweets)):
    #     print "Counting problem!"
    #     print "Number of tweets (%d) doesn't add up (%d, %d, %d)" % (num_tweets,
    #                                                                  num_positive_tweets,
    #                                                                  num_negative_tweets,
    #                                                                  num_neutral_tweets)
    #     sys.exit()
    #
    # most_positive_tweet = tweets.find_one({"sentiment": "positive"}, sort=[("score", -1)])
    # most_negative_tweet = tweets.find_one({"sentiment": "negative"}, sort=[("score", 1)])
    #
    # mean_results = tweets.aggregate([{"$group": {"_id": "$sentiment", "avgScore": {"$avg": "$score"}}}])
    # mean_results = list(mean_results)
    # print mean_results
    # # avg_pos_score = mean_results[1]['avgScore']
    # # avg_neg_score = mean_results[2]['avgScore']
    #
    # print "SENTIMENT BREAKDOWN"
    # print "Number (%%) of positive tweets: %d (%.2f%%)" % (
    #     num_positive_tweets, 100 * float(num_positive_tweets) / num_tweets)
    # print "Number (%%) of negative tweets: %d (%.2f%%)" % (
    #     num_negative_tweets, 100 * float(num_negative_tweets) / num_tweets)
    # print "Number (%%) of neutral tweets: %d (%.2f%%)" % (
    #     num_neutral_tweets, 100 * float(num_neutral_tweets) / num_tweets)
    # print ""

    # print "AVERAGE POSITIVE TWEET SCORE: %f" % float(avg_pos_score)
    # print "AVERAGE NEGATIVE TWEET SCORE: %f" % float(avg_neg_score)
    # print ""
    #
    # print "MOST POSITIVE TWEET"
    # print "Text: %s" % most_positive_tweet['text']
    # print "User: %s" % most_positive_tweet['screen_name']
    # print "Time: %s" % most_positive_tweet['time']
    # print "Score: %f" % float(most_positive_tweet['score'])
    # print ""
    #
    # print "MOST NEGATIVE TWEET"
    # print "Text: %s" % most_negative_tweet['text']
    # print "User: %s" % most_negative_tweet['screen_name']
    # print "Time: %s" % most_negative_tweet['time']
    # print "Score: %f" % float(most_negative_tweet['score'])
    return


if __name__ == "__main__":
    main()

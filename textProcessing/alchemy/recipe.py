#!/usr/bin/env python

#   Copyright 2015 AlchemyAI
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import sys
import urllib
from multiprocessing import Pool, Manager

import requests

from database.dbOperations import dbOperations as db
from database import dbOperations


def main():
    # Establish credentials for Twitter and AlchemyAPI
    credentials = get_credentials()
    sleepTweets = db("remote").returnDocsWithSpecificField("timelineDiagnosedUsers2")
    print len(sleepTweets)
    # Enrich the body of the Tweets using AlchemyAPI
    collection = []
    for tweet in sleepTweets:
        collection += [tweet]

    enriched_tweets = enrich(credentials, collection)
    #
    # # Store data in MongoDB
    store(enriched_tweets)
    #
    # # Print some interesting results to the screen
    print_results()
    return


def get_credentials():
    creds = {}
    creds['apikey'] = str()

    # If the file credentials.py exists, then grab values from it.
    # Values: "twitter_consumer_key," "twitter_consumer_secret," "alchemy_apikey"
    # Otherwise, the values are entered by the user
    try:
        import credentials

        creds['apikey'] = credentials.alchemy_apikey
    except:
        print "No credentials.py found"
        creds['apikey'] = raw_input("Enter your AlchemyAPI key: ")

    print "Using the following credentials:"
    print "\tAlchemyAPI key:", creds['apikey']

    # Test the validity of the AlchemyAPI key
    test_url = "http://access.alchemyapi.com/calls/info/GetAPIKeyInfo"
    test_parameters = {"apikey": creds['apikey'], "outputMode": "json"}
    test_results = requests.get(url=test_url, params=test_parameters)
    test_response = test_results.json()

    if 'OK' != test_response['status']:
        print "Oops! Invalid AlchemyAPI key (%s)" % creds['apikey']
        print "HTTP Status:", test_results.status_code, test_results.reason
        sys.exit()

    return creds


def enrich(credentials, tweets):
    # Prepare to make multiple asynchronous calls to AlchemyAPI
    apikey = credentials['apikey']
    pool = Pool(processes=10)
    mgr = Manager()
    result_queue = mgr.Queue()
    # Send each Tweet to the get_text_sentiment function
    for tweet in tweets:
        pool.apply_async(get_text_sentiment, (apikey, tweet, result_queue))

    pool.close()
    pool.join()
    collection = []
    while not result_queue.empty():
        collection += [result_queue.get()]

    print "Enrichment complete! Enriched %d Tweets" % len(collection)
    return collection


def get_text_sentiment(apikey, tweet, output):
    # Base AlchemyAPI URL for targeted sentiment call
    alchemy_url = "http://access.alchemyapi.com/calls/text/TextGetTextSentiment"

    # Parameter list, containing the data to be enriched
    parameters = {
        "apikey": apikey,
        "text": tweet['text'],
        "outputMode": "json",
        "showSourceText": 1
    }

    try:
        results = requests.get(url=alchemy_url, params=urllib.urlencode(parameters))
        response = results.json()
        print 'count'

    except Exception as e:
        print "Error while calling TextGetTargetedSentiment on Tweet (ID %s)" % tweet['id']
        print "Error:", e
        return

    try:
        if 'OK' != response['status'] or 'docSentiment' not in response:
            print "Problem finding 'docSentiment' in HTTP response from AlchemyAPI"
            print response
            print "HTTP Status:", results.status_code, results.reason
            print "--"
            return
        print "TWEEET", tweet
        tweet['sentiment'] = response['docSentiment']['type']
        tweet['score'] = 0.
        if tweet['sentiment'] in ('positive', 'negative'):
            tweet['score'] = float(response['docSentiment']['score'])
        output.put(tweet)

    except Exception as e:
        print "D'oh! There was an error enriching Tweet (ID %s)" % tweet['id']
        print "Error:", e
        print "Request:", results.url
        print "Response:", response

    return


def databaseInstance():
    db = dbOperations.dbOperations("local")
    return db


def store(tweets):
    for tweet in tweets:
        db("remote").updateDocumnet('timelineDiagnosedUsers2', {"_id": tweet['_id']}, {"$set": {"sentiment_alchemy": tweet["sentiment"]}})
    return


def print_results():
    # print ''
    # print ''
    # print '###############'
    # print '#    Stats    #'
    # print '###############'
    # print ''
    # print ''
    #
    # tweets = databaseInstance("alchemy")
    #
    # num_positive_tweets = tweets.find({"sentiment": "positive"}).count()
    # num_negative_tweets = tweets.find({"sentiment": "negative"}).count()
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

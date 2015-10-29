import twitter
import json
import time
import dbOperations
import tweetsOperations

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


class searchTweets():
    def __init__(self):
        self.count = 100

    # auth credentials
    consumer_key = 'qFrfx5pbJwrL2QxfzvLVufRVi'
    consumer_secret = '2Sq6lLxYZhMK2s5N57X5kvVDa8TTGFcgIuqBJpZ9Dufqv0NqWj'
    access_token = '3749211929-7efi0f7VxlllNEhpWslKTZqmt3bAqfEpZF0ZQlU'
    access_secret = 'OqFqVtS7srb0fuSIGXks9o5qFc8FNi5ScjkKogFLAWILG'

    auth = twitter.oauth.OAuth(access_token, access_secret, consumer_key, consumer_secret)
    global twitter_api, query1, query2
    twitter_api = twitter.Twitter(auth=auth)

    query1 = 'insomnia OR sleep issues OR wish i could sleep'
    query2 = 'sleeping pills OR sleeping'

    def requestNewTweets(self, query):
        tweets = twitter_api.search.tweets(q=query, count=self._count,result_type='mixed')
        return tweets

    def runTweets(self):
        self._count = 0
        self._maxId = 0
        self._tweetsReceived = []
        self._read = True
        self._numbValidTweets = 0
        tweetValidator = tweetsOperations.validators
        while (self._count < 20):

            print ("counter", self._count)
            try:
                if (self._read):
                    tweets = self.requestNewTweets(query1)
                    self._read = False
                    time.sleep(3)

                else:
                    tweets = self.requestNewTweets(query2)
                    self._read = True
                    time.sleep(3)

                for items in tweets['statuses']:
                    self._count += 1
                    self._tweetsReceived.append(items["text"])
                    dataJson = {'text': items["text"], "id": items["id"],'geo':items["geo"]}
                    print items['text']
                    print tweetsOperations.validators["Language"](items["text"])

                    if tweetValidator["Links"](items["text"]) or tweetValidator["Retweet"](items["text"]) or not tweetValidator["Language"](items["text"]):
                        print "Invalid Tweets"
                    else:
                        print "Valid tweet"
                        dbOperations.dbOperations().insertData(dataJson,"sleep")
                        self._numbValidTweets += 1
                #     with open('sampleTweetJson.txt', 'w') as outfile:
                #           json.dump(items, outfile,indent=1)
                #     break
                # break
            except Exception as e:
                print ("Exception", e)
                break


if __name__ == '__main__':
    # create a new fetcher
    newSearch = searchTweets()
    print "Searching tweets..."
    newSearch.runTweets()

# print json.dumps(statuses[0], indent=1)

# print 'Length: %s' % len(statuses)

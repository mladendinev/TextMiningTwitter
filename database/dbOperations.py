# __author__ = 'mladen'

import pymongo
from auth import Authentication
from bson.objectid import ObjectId
import json
from tweetsHelper import tweetsOperations
import codecs


class dbOperations(object):
    def __init__(self):
        try:
            self._configFile = "/home/mladen/TextMiningTwitter/configFiles/config.py"
            self._config = {}
            execfile(self._configFile, self._config)
            self.client = pymongo.MongoClient(
                'mongodb://' + self._config["username"] + ':' + self._config["password"] + '@127.0.0.1')
            self.db = self.client.SearchApiResults
            self.twitterApiAuth2 = Authentication.Authentication().twitterAuth()

        except Exception as e:
            print ("Exception Reading file"), e

    def countTweetsInDatabase(self, collection):
        try:
            numb = self.db[collection].count()
            return numb
        except Exception as e:
            print ("Find element operation exception", e)

    def returnAllTweetsFromCollection(self, collection):
        try:
            docs = self.db[collection].find()
            for doc in docs:
                return doc

        except Exception as e:
            print ("Find element operation exception", e)

    def returnLastIteration(self, collection):
        list = []
        maxElement = 0
        try:
            for doc in self.db[collection].find().sort('iteration', pymongo.ASCENDING):
                list.append(doc['iteration'])
                maxElement = max(list)
            return maxElement

        except Exception as e:
            print ("Find element operation exception", e)

    def findElementInCollection(self, collection, query):
        try:
            return self.db[collection].find_one(query)
        except Exception as e:
            print ("Find document operation exception", e)

    def getUserIds(self, collection):
        try:
            listIds = []
            for doc in self.db[collection].find():
                listIds.append(doc['userId'])
                return listIds
        except Exception as e:
            print ("Return ids exception", e)

    def updateDocumnet(self, collection, query, update):
        self.db[collection].update(query, update)

    def insertData(self, dataJson, collection):
        try:
            self.db[collection].insert(dataJson)
        except Exception as e:
            print ("Insert operation exception", e)

    def returnTweetsIds(self, id, collection):
        try:
            listIds = []
            myCursor = self.db[collection].find({type: id})
            while myCursor.hasNext():
                listIds.append(myCursor)
            return listIds
        except Exception as e:
            print "Iterating data failied", e

    def returnField(self, collection, field):
        try:
            listText = []
            count = 0
            for doc in self.db[collection].find({field: {'$exists': True}}):
                listText.append(doc[field])
                count += 1
                if count == 50:
                    break
            return listText


        except Exception as e:
            print "Iterating data failied", e

    def updateMissingFields(self, collection):
        try:
            countAll = 0
            countNone = 0
            for doc in self.db[collection].find({'utc_offset': {'$exists': False}}):
                tweetId = doc["tweet_id"]
                countAll += 1
                print countAll
                tweet = self.twitterApiAuth2.statuses.show(id=tweetId)
                if tweet == 1:
                    countNone += 1
                    print "count None", countNone
                    pass
                else:
                    self.db[collection].update({'_id': ObjectId(doc["_id"])},
                                               {'$set': {'utc_offset': tweet["user"]["utc_offset"],
                                                         'coordinates': tweet["coordinates"],
                                                         'place': tweet["place"]}})
            print countAll, countNone

        except Exception as e:
            print e

    def updateDiagnosticStatus(self, collection):
        try:
            countAll = 0
            countNone = 0
            for doc in self.db[collection].find():
                countAll += 1
                self.db[collection].update({'_id': ObjectId(doc["_id"])}, {'$set': {"diagnostic": None}}, upsert=False,
                                           multi=True)
            print countAll

        except Exception as e:
            print e

    def exportDiagnosticTweets(self, collection):
        try:
            with codecs.open('diagnostic_tweets', 'w', 'utf-8') as outfile:
                seen = set()
                for doc in self.db[collection].find({'diagnostic': "yes"}):
                    string = doc['text']
                    string = string.lower()
                    if string not in seen:
                        format = tweetsOperations.remove_emoji(string)
                        seen.add(format)
                        outfile.write(format + "\n")

        except Exception as e:
            print "Can't export diagnostic tweets", e

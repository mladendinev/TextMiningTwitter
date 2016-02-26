# __author__ = 'mladen'

import pymongo
from auth import Authentication
from bson.objectid import ObjectId
import json
from textProcessing import textPreprocessing
import codecs
from textProcessing import filters


class dbOperations(object):
    def __init__(self, database):
        try:
            if database == "local":
                self._configFile = "/home/mladen/TextMiningTwitter/configFiles/configLocal.py"
                self._config = {}
                execfile(self._configFile, self._config)
                self.client = pymongo.MongoClient(
                    'mongodb://' + self._config["username"] + ':' + self._config["password"] + '@127.0.0.1')
                self.twitterApiAuth2 = Authentication.Authentication().twitterAuth()
                self.db = self.client.SearchApiResults

            elif database == "remote":
                self._configFile = "/home/mladen/TextMiningTwitter/configFiles/configRemote.py"
                self._config = {}
                execfile(self._configFile, self._config)
                self.client = pymongo.MongoClient(
                    'mongodb://' + self._config["username"] + ':' + self._config[
                        "password"] + '@130.88.192.221' + ':27018')
                self.db = self.client.mbax2md2
                self.twitterApiAuth2 = Authentication.Authentication().twitterAuth()
            else:
                raise Exception("Non existent database")
        except Exception as e:
            print ("Exception Reading file"), e

    def countTweetsInDatabase(self, collection):
        try:
            numb = self.db[collection].count()
            return numb
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
            for doc in self.db[collection].find({field: {'$exists': True}}):
                listText.append(doc[field])
            return listText
        except Exception as e:
            print "Iterating data failied", e

    def returnObjectIds(self, collection, field):
        try:
            listText = []
            for doc in self.db[collection].find({"tweet_id": field}):
                listText.append(doc["_id"])
            return listText
        except Exception as e:
            print "Iterating data failied", e

    def deleteDocument(self, collection, listObjects):
        try:
            for objectId in listObjects:
                self.db[collection].remove({"$and": [{"_id": ObjectId(objectId)}, {"user": {"$exists": False}}]}, True)
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

    def updateCollection(self, collection, field, value):
        try:
            countAll = 0
            countNone = 0
            for doc in self.db[collection].find():
                countAll += 1
                self.db[collection].update({'_id': ObjectId(doc["_id"])}, {'$set': {field: value}}, upsert=False,
                                           multi=True)
            print countAll

        except Exception as e:
            print e

    def exportPositiveDiagnosticTweets(self, collection):
        try:
            with codecs.open('diagnostic_tweets', 'a', 'utf-8') as outfile:
                seen = set()
                users = ['rmorris', 'mladen', 'nberry']

                for user in users:
                    query = 'user.' + user + '.label'
                    print query
                    for doc in self.db[collection].find({query: "positive"}):
                        text = doc['text'].replace("\n", ' ')

                        # string = list(doc['text'])
                        # for i,char in string:
                        #     if string[i] == "\n":
                        #         string[i] = " "
                        # tweet=''.join(string)
                        tweet = text.lower()
                        outfile.write(tweet + "\n")

        except Exception as e:
            print "Can't export diagnostic tweets", e

    def returnFieldIteration(self, collection, matchField, sortingField):
        print matchField
        for doc in self.db[collection].aggregate([{"$match": {"search_terms": matchField}},
                                                  {"$sort": {sortingField: -1}},
                                                  {"$limit": 1},
                                                  {"$project": {sortingField: 1, "search_terms": 1}}], useCursor=False):
            return doc['iteration']

    def returnSleepTweets(self, collection, field, value):
        collumns = []
        index = []
        for doc in self.db[collection].find({field: value}):
            collumns.append({'text': doc['text'], "sentiment": doc['sentiment'], 'label': value})
        return collumns

    def returnDocsWithSpecificField(self, collection, field, value):
        dictTweets = []
        for tweet in self.db[collection].find({field: value}):
            dictTweets.append(tweet)
        return dictTweets

    def updateDiagnosticPotentialTweets(self, collection):
        for tweet in self.db[collection].find():
            if filters.filterPotentialDiagnostic(tweet["text"]):
                self.db[collection].update({'_id': ObjectId(tweet["_id"])}, {'$set': {"potentialDiagnostic": "yes"}},
                                           upsert=False,
                                           multi=False)

    def exportRohanTweets(self, collection):

        all = []
        for tweet in self.db[collection].find(
                {"$and": [{"user.rmorris": {"$exists": True}}, {"user.nberry": {"$exists": False}}]}):
            tweets = []
            tweets.append(tweet['text'])
            tweets.append(tweet['user']['rmorris']['label'])
            all.append(tweets)
        return all

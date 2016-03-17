# -*- coding: utf-8 -*-
__author__ = 'mladen'
import json
import codecs
from collections import Counter

import pymongo
from bson.objectid import ObjectId

from sentiStrength.run import PythonWrapSentiment
from auth import Authentication
from textProcessing import textPreprocessing
from textProcessing import filters
from textProcessing.informationRetrieval import IR
from TweetNLP import CMUTweetTagger


class dbOperations:
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
            for doc in self.db[collection].find({'location': {'$exists': False}}):
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
                                               {'$set': {'location': tweet["user"]["location"]}})
                    # 'coordinates': tweet["coordinates"],
                    # 'place': tweet["place"]}})
            print countAll, countNone

        except Exception as e:
            print e
            pass


    def exportPositiveDiagnosticTweets(self, collection):
        try:
            with codecs.open('diagnostic_tweets', 'a', 'utf-8') as outfile:
                seen = set()
                users = ['rmorris', 'mladen', 'nberry']

                for user in users:
                    query = 'user.' + user + '.label'
                    for doc in self.db[collection].find({query: "positive"}):
                        text = doc['text'].replace("\n", ' ')

                        # string = list(doc['text'])
                        # for i,char in string:
                        #     if string[i] == "\n":
                        #         string[i] = " "
                        # tweet=''.join(string)
                        text = textPreprocessing.analyseText(text)
                        tweet = text.lower()
                        outfile.write(tweet + "\n")

        except Exception as e:
            print "Can't export diagnostic tweets", e

    def returnFieldIteration(self, collection, matchField, sortingField):
        for doc in self.db[collection].aggregate([{"$match": {"search_terms": matchField}},
                                                  {"$sort": {sortingField: -1}},
                                                  {"$limit": 1},
                                                  {"$project": {sortingField: 1, "search_terms": 1}}], useCursor=False):
            return doc['iteration']

    def returnInfoExtraction(self, collection, user1, query):
        collumns = []
        for doc in self.db[collection].find(query):
            collumns.append(
                {'text': doc['text'], 'label': user1,
                 'tweet_id': doc['tweet_id'],
                 "pos_tags": doc['pos_tags'],
                 'freq_pos': doc["freq_pos"],
                 'labeled_entities': doc['labeled_entities'],
                 'unlabeled_entities': doc['unlabeled_entities'],
                 'pod': doc['pod'], 'semantic_class': doc['semantic_class'],
                 'min_after_midnight': doc['min_after_midnight'],
                 })
        return collumns

    #

    def returnDocsWithSpecificField(self, collection):
        dictTweets = []
        for tweet in self.db[collection].find():
            dictTweets.append(tweet)
        return dictTweets

    def returnDocsForTimelineExt(self, collection, field, value):
        dictTweets = []
        for tweet in self.db[collection].find({"$and": [{field: value}, {"processedTimeline": {"$exists": False}}]}):
            dictTweets.append(tweet)
        return dictTweets

    def updateDiagnosticPotentialTweets(self, collection):
        for tweet in self.db[collection].find():
            if filters.filterPotentialDiagnostic(tweet["text"]):
                self.db[collection].update({'_id': ObjectId(tweet["_id"])}, {'$set': {"potentialDiagnostic": "yes"}},
                                           upsert=False,
                                           multi=False)

    def transferTweets(self):
        try:
            allTweetIds = []
            for tweet in self.db["rohanDataset"].find({"diagnostic": "Yes"}):
                if tweet['id'] not in allTweetIds:
                    allTweetIds.append(tweet['id'])
                    saveDataToJson = {'text': tweet["text"],
                                      "tweet_id": tweet["id"],
                                      'geo': tweet["geo"],
                                      'userId': tweet["user"]["id"],
                                      'created_at': tweet["created_at"],
                                      'time_zone': tweet["user"]["time_zone"],
                                      "utc_offset": tweet["user"]["utc_offset"],
                                      'place': tweet["place"],
                                      'coordinates': tweet["coordinates"],
                                      'extraData': 'positve'}

                    self.db['diagnosticTweets'].insert(saveDataToJson)

            for tweet in self.db["andrewDataset"].find({"diagnostic": "Yes"}):
                if tweet['id'] not in allTweetIds:
                    allTweetIds.append(tweet['id'])
                    saveDataToJson = {'text': tweet["text"],
                                      "tweet_id": tweet["id"],
                                      'geo': tweet["geo"],
                                      'userId': tweet["user"]["id"],
                                      'created_at': tweet["created_at"],
                                      'time_zone': tweet["user"]["time_zone"],
                                      "utc_offset": tweet["user"]["utc_offset"],
                                      'place': tweet["place"],
                                      'coordinates': tweet["coordinates"],
                                      'extraData': 'positve'}

                    self.db['diagnosticTweets'].insert(saveDataToJson)
        except Exception as e:
            print e

    #########################################Information Extraction###################################################

    def extractLocalTime(self, collection):
        global localtime
        for doc in self.db[collection].find():
            if doc['coordinates'] != None:
                if doc['coordinates']['type'] == 'Point':
                    localtime = IR.get_timezone(doc['coordinates']['coordinates'], doc["created_at"])
            elif doc["utc_offset"] != None:
                localtime = IR.calculate_localtime(doc["created_at"], doc["utc_offset"])
            elif doc["time_zone"] != None:
                localtime = IR.convertTimezoneToLocal(doc["time_zone"],doc["created_at"])
            else:
                localtime = None
            self.db[collection].update({'_id': ObjectId(doc["_id"])}, {'$set': {"local_time_tweet": localtime}},
                                           upsert=False,
                                           multi=True)

    def convertTimeToMins(self,collection):
        for doc in self.db[collection].find():
            if doc["local_time_tweet"] !=None:
                convertTime = IR.minutes_after_midnight(doc["local_time_tweet"])
                self.db[collection].update({'_id': ObjectId(doc["_id"])}, {'$set': {"min_after_midnight": convertTime}},
                                           upsert=False,
                                           multi=True)


    def pos_tagging(self, collection):
        feature_vector = []
        counter = 0
        for doc in self.db[collection].find(
                {"$and": [{"user.rmorris.label": {"$exists": True}}, {"user.nberry.label": {"$exists": False}}]}):
            result = textPreprocessing.tokenizeText(doc['text'])
            result = CMUTweetTagger.runtagger_parse(result)
            tags = [[x[1] for x in word] for word in result]
            tags = [tag[0] for tag in tags]
            freq = Counter(tags).most_common(2)
            pos_tags = json.dumps(tags)
            frequency = json.dumps(freq)
            self.db[collection].update({'_id': ObjectId(doc["_id"])},
                                       {'$set': {"pos_tags": pos_tags, "freq_pos": frequency}}, upsert=False,
                                       multi=True)


    def updateCommon(self, collection):
        counter = 0
        for doc in self.db[collection].find({"potentialDiagnostic": {"$exists": True}}):
            if counter < 10:
                self.db[collection].update({'_id': ObjectId(doc["_id"])},
                                           {'$set': {"common": "yes"}}, upsert=False,
                                           multi=True)
                counter += 1
            else:
                break

    def name_entity(self, collection):
        counter = 0
        for doc in self.db[collection].find():
            print counter
            unlabelled_entity_names = textPreprocessing.unlabelled_entity_names(doc['text'])
            tagged_tweet = textPreprocessing.tagg_tweet(doc['text'])
            labeled_entity = textPreprocessing.label_entity(tagged_tweet)
            self.db[collection].update({'_id': ObjectId(doc["_id"])},
                                       {'$set': {"labeled_entities": labeled_entity,
                                                 "unlabeled_entities": unlabelled_entity_names}}, upsert=False,
                                       multi=True)
            counter += 1

    def semantic_classes(self, collection):
        for doc in self.db[collection].find():
            listEntry = []
            for semantic in self.db['semantic_classes'].find():
                normalisedEntity = [x.lower() for x in semantic['entities']]
                normalisedText = [x.lower() for x in textPreprocessing.tokenizeText(doc['text'])]
                interesection = list(set(normalisedEntity) & set(normalisedText))
                if interesection:
                    for element in interesection:
                        data = {semantic['name']: element}
                        listEntry.append(data)

            self.db[collection].update({'_id': ObjectId(doc['_id'])},
                                       {'$set': {"semantic_class": listEntry}},
                                       upsert=False,
                                       multi=True)

    def findAndReturn(self,collection,query):
        output = []
        for doc in self.db[collection].find(query):
            output.append(doc)
        return output


    def sentimentPolarity(self,collection):
        counter = 0
        for doc in self.db[collection].find({"sentiment_strength":{"$exists":False}}):
            tweet = textPreprocessing.normSentiment(doc['text']).encode('ascii', 'ignore')
            if len(tweet) > 1:
                sentiment = PythonWrapSentiment().RateSentiment(tweet)
                self.db[collection].update({'_id': ObjectId(doc['_id'])},
                                           {'$set': {"sentiment_strength": sentiment}},
                                           upsert=False,
                                           multi=True)

    def semanticVariety(self,collection):
        varietySemantic = []
        for doc in self.db[collection].find():
            if doc["semantic_class"]:
                for dictionary in doc['semantic_class']:
                    for key in dictionary:
                        varietySemantic.append(key)
        return Counter(varietySemantic)

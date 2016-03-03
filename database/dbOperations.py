__author__ = 'mladen'

import json
import codecs
from collections import Counter

import pymongo
from bson.objectid import ObjectId

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

    def returnSpecTweets(self, collection, user, query):
        collumns = []
        for doc in self.db[collection].find(query):
            collumns.append(
                # {'text': doc['text'], 'label': value, "tweet_id": doc['tweet_id'], 'created_at': doc["created_at"],
                #  'time_zone': doc['time_zone'], 'utc_offset': doc['utc_offset']})
                {'text': doc['text'], 'label': user,'tweet_id':doc['tweet_id'], "pos_tags": doc['pos_tags'], 'freq_pos': doc["freq_pos"],
                 'labeled_entities': doc['labeled_entities'], 'unlabeled_entities': doc['unlabeled_entities']})
        return collumns

    #

    def returnDocsWithSpecificField(self, collection, field, value):
        dictTweets = []
        for tweet in self.db[collection].find({field: value}):
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

    def exportRohanTweets(self, collection):

        all = []
        for tweet in self.db[collection].find(
                {"$and": [{"user.rmorris": {"$exists": True}}, {"user.nberry": {"$exists": False}}]}):
            tweets = []
            tweets.append(tweet['text'])
            tweets.append(tweet['user']['rmorris']['label'])
            all.append(tweets)
        return all

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
        for doc in self.db[collection].find():
            if doc["utc_offset"] != None:
                localtime = IR.calculate_localtime(doc["created_at"], doc["utc_offset"])
                if localtime == None:
                    pod = None
                else:
                    pod = IR.get_part_of_the_day(localtime)
            elif doc["time_zone"] != None:
                localtime = IR.convertTimezoneToLocal(doc["time_zone"])
                if localtime == None:
                    pod = None
                else:
                    pod = IR.get_part_of_the_day(localtime)
            else:
                pod = None

            self.db[collection].update({'_id': ObjectId(doc["_id"])}, {'$set': {"pod": pod}}, upsert=False,
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
            print 'Tag'
            self.db[collection].update({'_id': ObjectId(doc["_id"])},
                                       {'$set': {"pos_tags": pos_tags, "freq_pos": frequency}}, upsert=False,
                                       multi=True)

    def pos_tagging2(self, collection):
        for doc in self.db[collection].find({"second": {"$exists": True}}):
            list = json.loads(doc['second'])

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

# sentences = nltk.sent_tokenize(text)
# tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
# tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
# chunked_sentences = nltk.ne_chunk(tagged_sentences, binary=True)
# print chunked_sentences
# print 'hui'
# entity_names = []
#
# if hasattr(chunked_sentences, 'label') and chunked_sentences.label:
#     if chunked_sentences.label() == 'NE':
#         entity_names.append(' '.join([child[0] for child in chunked_sentences]))
#     else:
#         for child in chunked_sentences:
#             entity_names.extend(self.extract_entity_names(child))
#
# return entity_names

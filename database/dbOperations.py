# __author__ = 'mladen'

import pymongo
import json
import sys


class dbOperations(object):
    def __init__(self):
        try:
            self._configFile = "/home/mladen/FinalYearProject/conifigDb/config.py"
            self._config = {}
            execfile(self._configFile, self._config)
            self.client = pymongo.MongoClient(
                'mongodb://' + self._config["username"] + ':' + self._config["password"] + '@127.0.0.1')
            self.db = self.client.SearchApiResults
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
                self.db[collection].find()
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
             return  self.db[collection].find_one(query)
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


    def updateDocumnet(self,collection, query, update):
        self.db[collection].update(query, update)

    def insertData(self, dataJson, collection):
        try:
            self.db[collection].insert(dataJson)
        except Exception as e:
            print ("Insert operation exception", e)

    def iterateThroughElemets(self, id):
        try:
            listIds = []
            myCursor = self.db.testing123.find({type: id})
            while myCursor.hasNext():
                listIds.append(myCursor)
            return listIds
        except Exception as e:
            print "Iterating data failied", e

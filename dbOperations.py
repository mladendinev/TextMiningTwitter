# __author__ = 'mladen'

import pymongo
import json

class dbOperations(object):

    def __init__(self):
        self._config = {}
        execfile("configDb.py",self._config)
        self.client = pymongo.MongoClient('mongodb://' + self._config["username"] + ':'+ self._config["password"]+'@127.0.0.1')
        self.db = self.client.SearchApiResults
        #self.db = pymongo.MongoClient.textMiningStreamr

    def countTweetsInDatabase(self, collection):
        numb = self.db[collection].count()
        return numb

    def returnAllTweetsFromCollection(self, collection):
        try:
            self.db[collection].find()
        except Exception as e:
            print ("Find element operation exception", e)

    def findElementInCollection(self,collection,query):
          return self.db[collection].find(query)

    def insertData(self,dataJson, collection):
        try:
            if collection == "sleep":
              self.db.sleepTweets.insert(dataJson)
        except Exception as e:
            print ("Insert operation exception", e)

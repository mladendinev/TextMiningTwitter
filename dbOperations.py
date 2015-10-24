__author__ = 'mladen'

import pymongo

db = pymongo.MongoClient().textMiningStream

def countTweetsInDatabase(self, collection):
    numb = db[collection].count()
    return numb


def returnAllTweets(self, collection):
    db[collection].find()

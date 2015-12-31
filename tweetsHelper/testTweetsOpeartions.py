__author__ = 'mladen'
import tweetsOperations
import semanticFunc
from database import dbOperations

class testTweetsOperations():
    if __name__ == "__main__":
        tweetsOps = tweetsOperations
        extract = semanticFunc
        # listTweets = dbOperations.dbOperations().returnField("diagnosticTweets","text")
        text = "RT @John Sanchez is the best football player #Arsenal http://arsenal.com/stats"
        # print extract.stemming(text)
        print extract.tfidfFunc()
        # print extract.extractEntities(listTweets)
        # print tweetsOperations.analyseText(text)

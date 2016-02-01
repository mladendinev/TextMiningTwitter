__author__ = 'mladen'
import tweetsOperations
import semanticFunc
import NegationDetection
from database import dbOperations

class testTweetsOperations():
    if __name__ == "__main__":
        tweetsOps = tweetsOperations
        negation = NegationDetection
        extract = semanticFunc
        # listTweets = dbOperations.dbOperations().returnField("diagnosticTweets","text")
        # diagnosticTweets = dbOperations.dbOperations().exportDiagnosticTweets("diagnosticTweets")
        text1 = "RT @John Sanchez is the best football player #Arsenal http://arsenal.com/stats"
        text2 = "I love cats"
        text3 = "I wasn't diagnosed with schizofrenia, I wasn't sick"
        text4 = "Wrongly diagnosed with psychotic disorder"
        # negation.negationDetection(text4)
        # print extract.stemming(text)
        # negation.findSynsets(text2)
        negation.findSimilarityInSynsets()
        # extract.testScit()
        # print extract.extractEntities(listTweets)
        # print tweetsOperations.analyseText(text1)

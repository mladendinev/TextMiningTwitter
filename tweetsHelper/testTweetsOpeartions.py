__author__ = 'mladen'
import tweetsOperations
import semanticFunc

class testTweetsOperations():
    if __name__ == "__main__":
        tweetsOps = tweetsOperations
        extract = semanticFunc

        text = "RT @John Sanchez is the best football player #Arsenal http://arsenal.com/stats"
        # print extract.stemming(text)
        print extract.tfidfFunc()
        # print tweetsOperations.analyseText(text)

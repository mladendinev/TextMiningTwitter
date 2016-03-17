__author__ = 'mladen'
import codecs
from database import dbOperations


class exportRohanTweets():
    def exportTweets(self):
        tweets = dbOperations.dbOperations("remote").exportRohanTweets("diagnosticTweets")
        print tweets
        with codecs.open('rohan_diagnostic', 'a', 'utf-8') as outfile:
            for tweet in tweets:
                outfile.write(tweet[0] + "\n"+ tweet[1] + "\n")

if __name__ == "__main__":
    exp = exportRohanTweets()
    exp.exportTweets()
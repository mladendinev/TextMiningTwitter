__author__ = 'mladen'
import textPreprocessing
import tfidf
import negationDetection
from database import dbOperations
import filters


class testTweetsOperations():
    if __name__ == "__main__":
        text1 = "RT @John Sanchez is the best football player #Arsenal http://arsenal.com/stats"
        text2 = "love cats"
        text3 = "I wasn't diagnosed with schizofrenia, I wasn't sick"
        text4 = "Wrongly diagnosed with psychotic disorder btw Latuda ours"
        test = textPreprocessing
        negation = negationDetection
        extract = tfidf

        # test.replaceAbbreviation(text4)
        # test.lemmatization(text2)
        # listTweets = dbOperations.dbOperations().returnField("diagnosticTweets","text")
        # diagnosticTweets = dbOperations.dbOperations("local").updateCollection("sleepTweetsTest", "sleepRelated", None)
        # negation.negationDetection(text4)
        # print extract.stemming(text)
        # negation.findSynsets(text2)
        # negation.findSimilarityInSynsets()
        # print extract.extractEntities(listTweets)
        # print tweetsOperations.analyseText(text1)

        # potentialTweets = dbOperations.dbOperations("remote").updateDiagnosticPotentialTweets("diagnosticTweets")
        try:
            sleepTweets = dbOperations.dbOperations("remote").returnField("sleepTweetsTestLocal", "tweet_id")
            # sleepTweets = dbOperations.dbOperations("remote").findElementInCollection\
            #                                 ("sleepTweetsTestLocal", {"tweet_id":(long)(700415722300768256)})
            # if sleepTweets == None:
            #     print 'ok'
            # print sleepTweets


            ############################# FINDING DUPLICATES #############################################

            def list_duplicates(seq):
                seen = set()
                seen_add = seen.add
                seen_twice = set(x for x in seq if x in seen or seen_add(x))
                # turn the set into a list (as requested)
                return list(seen_twice)

            #
            duplicatedTweetIds = list_duplicates(sleepTweets)
            print len(duplicatedTweetIds)
            print  duplicatedTweetIds[10]
            # for duplicate in duplicatedTweetIds:
            #     duplicatedObjectIds = dbOperations.dbOperations("remote").returnObjectIds("sleepTweetsTestLocal",
            #                                                                               duplicate)
            #     head, tail = duplicatedObjectIds[0], duplicatedObjectIds[1:]
            #     dbOperations.dbOperations("remote").deleteDocument("sleepTweetsTestLocal", tail)

        except Exception, e:
            print e
            #

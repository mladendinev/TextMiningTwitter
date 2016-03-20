__author__ = 'mladen'
import textPreprocessing
import tfidf
import negationDetection
from database import dbOperations


class testTweetsOperations():
    if __name__ == "__main__":
        text1 = "RT @John Sanchez is the best football player #Arsenal http://arsenal.com/stats"
        text2 = "I don't like cats"
        hui2 = 'I was in Nebraska for 1 month. I played football for 10 weeks'
        text3 = "I wasn't diagnosed with schizofrenia, I wasn't sick and healthy"
        text4 = "Wrongly diagnosed with psychotic. Disorder btw Latuda ours"
        text5 = "I keep waking up at like 3 am starving and i fall back asleep because so the hungry u'\U0001f62d\U0001f62d\U0001f62d\U0001f62d"

        test = textPreprocessing
        negation = negationDetection
        extract = tfidf

        # test.replaceAbbreviation(text4)
        # test.lemmatization(text2)
        # listTweets = dbOperations.dbOperations().returnField("diagnosticTweets","text")
        # diagnosticTweets = dbOperations.dbOperations("remote").updateMissingFields("diagnosticTweets")
        # negation.negationDetection(text4)
        # print extract.stemming(text)
        # negation.findSynsets(text2)
        # negation.findSimilarityInSynsets()
        # print extract.extractEntities(listTweets)

        # print  featureExtraction.sentiment_score(text2)
        # up = dbOperations.dbOperations("remote").updateCommon("diagnosticTweets")

        #dbOperations.dbOperations("remote").UpdateSemanticTrends()
        #dbOperations.dbOperations("remote").semantic_classes('timelineDiagnosedUsers2')
        # dbOperations.dbOperations("remote").semantic_classes('AnnotatedDiagnosticData')
        # dbOperations.dbOperations("remote").semantic_classes('diagnosticTweets')
       # dbOperations.dbOperations("remote").semantic_classes('sleepTweetsTestLocal')
        # from textProcessing import featureExtraction
        # featureExtraction.sentiment_score()

        #print visualiseStats.overallStatistics()

        # tag = CMUTweetTagger.runtagger_parse(textPreprocessing.normaliseText(text1))
        # a = [[('k')]]
        # print len(tag)
        # print len(a)
        # try:



        ########################### FINDING DUPLICATES #############################################
        # sleepTweets = dbOperations.dbOperations("remote").returnField("timelineDiagnosedUsers2", "tweet_id")
        #
        # def list_duplicates(seq):
        #     seen = set()
        #     seen_add = seen.add
        #     seen_twice = set(x for x in seq if x in seen or seen_add(x))
        #     # turn the set into a list (as requested)
        #     return list(seen_twice)
        #
        #
        # duplicatedTweetIds = list_duplicates(sleepTweets)
        # print len(duplicatedTweetIds)
        # print [item for item, count in collections.Counter(duplicatedTweetIds).items() if count > 1]
        # for duplicate in duplicatedTweetIds:
        #     duplicatedObjectIds = dbOperations.dbOperations("remote").returnObjectIds("timelineDiagnosedUsers2",
        #                                                                               duplicate)
        #     head, tail = duplicatedObjectIds[0], duplicatedObjectIds[1:]
        #     dbOperations.dbOperations("remote").deleteDocument("timelineDiagnosedUsers2", tail)
        #


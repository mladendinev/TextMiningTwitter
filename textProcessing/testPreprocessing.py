__author__ = 'mladen'
import textPreprocessing
import tfidf
import negationDetection


class testTweetsOperations():
    if __name__ == "__main__":

        hui = u'Summer School of the Arts filling fast\nWanganui people have the chance to learn the intricacies of decorative sugar art from one of the country\xe2\x80\x99s top pastry chefs at Whanganui UCOL\xe2\x80\x99s Summer School of the Arts in January.\nTalented Chef de Partie, Adele Hingston will take time away from her duties at Christchurch\xe2\x80\x99s Crowne Plaza to demonstrate the tricks and techniques of cake decorating including creating flower sprays and an introduction to royal icing.\nDemand has been high for places in the Summer School of the Arts but there are still opportunities for budding artists to hone their skills in subjects as diverse as jewellery making, culinary sugar art and creative writing. \n\xe2\x80\x9cThe painting, pattern drafting and hot glass classes filled almos'
        text1 = "RT @John Sanchez is the best football player #Arsenal http://arsenal.com/stats"
        text2 = "I don't like cats"
        hui2 = 'I was in Nebraska for 1 month. I played football for 10 weeks'
        text3 = "I wasn't diagnosed with schizofrenia, I wasn't sick"
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
        # kur = dbOperations.dbOperations("remote").name_entity("sleepTweetsTestLocal")
        op = textPreprocessing.removePunctuation(text2)
        print op
        # laino = CMUTweetTagger.runtagger_parse(textPreprocessing.normaliseText(text1))
        # print laino
        # a = [[('k')]]
        # print len(laino)
        # print len(a)
        # try:
        #     sleepTweets = dbOperations.dbOperations("remote").returnField("streamDiagnostic", "tweet_id")


        ############################# FINDING DUPLICATES #############################################
        #
        # def list_duplicates(seq):
        #     seen = set()
        #     seen_add = seen.add
        #     seen_twice = set(x for x in seq if x in seen or seen_add(x))
        #     # turn the set into a list (as requested)
        #     return list(seen_twice)

        #
        # duplicatedTweetIds = list_duplicates(sleepTweets)
        # print len(duplicatedTweetIds)
        # print [item for item, count in collections.Counter(duplicatedTweetIds).items() if count > 1]
        # for duplicate in duplicatedTweetIds:
        #     duplicatedObjectIds = dbOperations.dbOperations("remote").returnObjectIds("sleepTweetsTestLocal",
        #                                                                               duplicate)
        #     head, tail = duplicatedObjectIds[0], duplicatedObjectIds[1:]
        #     dbOperations.dbOperations("remote").deleteDocument("sleepTweetsTestLocal", tail)

        # except Exception, e:
        #     print e
        #


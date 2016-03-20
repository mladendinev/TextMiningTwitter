__author__ = 'mladen'

from collections import Counter
import random

import nltk
from nltk.corpus import sentiwordnet as swn
from nltk.corpus import wordnet as wn
import dataAnalysis
from textProcessing import textExtractor
import numpy as np
sleepDrugs = "/home/mladen/TextMiningTwitter/word_lists/sleepDrugs.txt"

########################################################################################################################
#################### THE METHODS EXTRACT THE FEATURE DIRECTLY FROM THE ALREADY PRE-PROCESSED DATABASE JSON##############
######################################################################################

###############TEXT EXTRACTOR#########################
def textTweets():
    data = dataAnalysis.trainingData()
    timeline = dataAnalysis.timelineTweets
    seen = []
    negativeExamples = []
    positiveExamples = []
    testing = []
    global tupple
    for tweet in data[0]:
        if tweet["tweet_id"] not in seen:
            seen.append(tweet["tweet_id"])
            tupple = (tweet['text'], 'pos')
            positiveExamples.append(tupple)

    for tweet in data[1]:
        if tweet["tweet_id"] not in seen:
            seen.append(tweet["tweet_id"])
            tupple = (tweet['text'], 'neg')
            negativeExamples.append(tupple)

    for tweet in timeline:
        # if tweet["tweet_id"] in seen:
        #     print "already seen : %s" % tweet['tweet_id']
        seen.append(tweet["tweet_id"])
        entry = (tweet['text'])
        testing.append(entry)
    print "Number negative annotated", len(negativeExamples)
    print "Number positive annotated", len(positiveExamples)
    print "Number testing tweets", len(positiveExamples)
    return positiveExamples + negativeExamples, testing


def surrounding_words(iterable):
    iterator = iter(iterable)
    prev = None
    item = iterator.next()  # throws StopIteration if empty.
    for next in iterator:
        yield (prev, item, next)
        prev = item
        item = next
    yield (prev, item, None)


###############POS EXTRACTOR#########################
def pos_tags():
    data = dataAnalysis.trainingData()
    timeline = dataAnalysis.timelineTweets
    seen = []
    negativeExamples = []
    positiveExamples = []
    testing = []
    textTweet = []
    global counter
    global tupple
    for tweet in data[0]:
        if tweet["tweet_id"] not in seen:
            seen.append(tweet["tweet_id"])
            if 'pos_tags' in tweet:
                tweet_pos_tags = tweet['pos_tags'] or []
                pos_tag = [element[1] for element in tweet_pos_tags]
                counter = Counter(pos_tag)
                tupple = (counter, 'pos')
                positiveExamples.append(tupple)


    for tweet in data[1]:
        if tweet["tweet_id"] not in seen:
            seen.append(tweet["tweet_id"])
            if 'pos_tags' in tweet:
                tweet_pos_tags = tweet['pos_tags'] or []
                pos_tag = [element[1] for element in tweet_pos_tags]
                counter = Counter(pos_tag)
                tupple = (counter, 'neg')
                negativeExamples.append(tupple)

    for tweet in timeline:
        if 'pos_tags' in tweet:
            tweet_pos_tags = tweet['pos_tags'] or []
            textTweet.append(tweet["text"])
            pos_tag = [element[1] for element in tweet_pos_tags]
            counter = Counter(pos_tag)
            testing.append(counter)
    print "Number negative annotated", len(negativeExamples)
    print "Number positive annotated", len(positiveExamples)
    print "Number testing tweets", len(positiveExamples)
    return positiveExamples + negativeExamples, testing, textTweet


###############SEMANTIC CLASSES EXTRACTOR#########################
def semantic_classes():
    data = dataAnalysis.trainingData()
    timeline = dataAnalysis.timelineTweets
    seen = []
    negativeExamples = []
    positiveExamples = []
    testingExamples = []
    text = []
    global tupple
    for tweet in data[0]:
        if tweet["tweet_id"] not in seen:
            seen.append(tweet["tweet_id"])
            if 'semantic_class' in tweet:
                semantic_words = tweet['semantic_class'] or []
                # # finalMap = {}
                if semantic_words:
                    #     for d in semantic_words:
                    # print d
                    # print tweet['semantic_class']
                    # print tweet['tweet_id']
                    # finalMap.update(d)
                    tupple = (semantic_words, 'pos')
                else:
                    tupple = (Counter(),'pos')
                positiveExamples.append(tupple)

    for tweet in data[1]:
        if tweet["tweet_id"] not in seen:
            seen.append(tweet["tweet_id"])
            if 'semantic_class' in tweet:
                semantic_words = tweet['semantic_class'] or []
                # finalMap = {}
                if semantic_words:
                #     #     for d in semantic_words:
                #     #         finalMap.update(d)
                    tupple = (semantic_words, 'neg')
                else:
                    tupple = (Counter(), 'neg')
                negativeExamples.append(tupple)

    for tweet in timeline:
        if 'semantic_class' in tweet:
            semantic_words = tweet['semantic_class'] or []
            text.append(tweet["text"])
            # finalMap = {}
            if semantic_words:
                #     for d in semantic_words:
                #         finalMap.update(d)
                entry = semantic_words
            else:
                entry = (Counter())
            testingExamples.append(entry)

    print "Number negative annotated", len(negativeExamples)
    print "Number positive annotated", len(positiveExamples)
    return positiveExamples + negativeExamples, testingExamples, text



###############POS FREQUENCY EXTRACTOR#########################
def pos_tags_frequency():
    data = dataAnalysis.trainingData()
    seen = []
    timeline = dataAnalysis.timelineTweets
    testing = []
    negativeExamples = []
    positiveExamples = []
    text = []
    global counter
    global tupple
    for tweet in data[0]:
        if tweet["tweet_id"] not in seen:
            seen.append(tweet["tweet_id"])
            if 'pos_tags' in tweet:
                tweet_pos_tags = tweet['pos_tags'] or []
                pos_tag = [element[1] for element in tweet_pos_tags]
                counter = Counter(pos_tag)
                if len(counter) >= 2:
                    counter = counter.most_common(2)
                    tupple = (dict(counter), 'pos')
                    positiveExamples.append(tupple)
                    random.shuffle(positiveExamples)

    for tweet in data[1]:
        if tweet["tweet_id"] not in seen:
            seen.append(tweet["tweet_id"])
            if 'pos_tags' in tweet:
                tweet_pos_tags = tweet['pos_tags'] or []
                pos_tag = [element[1] for element in tweet_pos_tags]
                counter = Counter(pos_tag)
                if len(counter) >= 2:
                    counter = counter.most_common(2)
                    tupple = (dict(counter), 'neg')
                    negativeExamples.append(tupple)
                    random.shuffle(negativeExamples)

    for tweet in timeline:
        if 'pos_tags' in tweet:
            tweet_pos_tags = tweet['pos_tags'] or []
            pos_tag = [element[1] for element in tweet_pos_tags]
            counter = Counter(pos_tag)
            if len(counter) >= 2:
                text.append(tweet["text"])
                counter = counter.most_common(2)
                testing.append(dict(counter))

    print "Number negative annotated", len(negativeExamples)
    print "Number positive annotated", len(positiveExamples)
    print "Number testing tweets", len(positiveExamples)
    return positiveExamples + negativeExamples, testing, text


#########SENTIMENT SCORE FEATURE EXTRACTOR############################
def sentiment_score():
    data = dataAnalysis.trainingData()
    timeline = dataAnalysis.timelineTweets
    positiveExamples = []
    negativeExamples = []
    seen = []
    tweetsText = []
    testingExamples = []
    sentiment_score_tweet = 0
    global polarity_of_word
    adverbs = ['pretty', 'fairly', 'really', 'very', 'quite']
    ###########Positive labels from th
    for tweet in data[0]:
        if tweet["tweet_id"] not in seen:
            seen.append(tweet["tweet_id"])
            if 'pos_tags' in tweet:
                wordsInTweet = tweet['pos_tags'] or []
                # wordsInTweet = tweet["pos_tags"]
                sentiment_score_tweet = 0
                if wordsInTweet:
                    for k,pair in enumerate(wordsInTweet):
                        wordSentimentScore = sentimentScoreFromSynonyms(pair[0], pair[1])
                        # if k>0 and (wordsInTweet[k-1][0] in adverbs):
                        #     if wordSentimentScore> 0:
                        #         wordSentimentScore += 0.2
                        #     elif wordSentimentScore < 0:
                        #         wordSentimentScore -= 0.2
                        sentiment_score_tweet += wordSentimentScore
                    tupple = ({"sentiment_score": sentiment_score_tweet}, "pos")

                else:
                    tupple = ({"sentiment_score": 0}, "pos")
                positiveExamples.append(tupple)

    for tweet in data[1]:
        if tweet["tweet_id"] not in seen:
            seen.append(tweet["tweet_id"])
            if 'pos_tags' in tweet:
                wordsInTweet = tweet['pos_tags'] or []
                # wordsInTweet = tweet["pos_tags"]
                sentiment_score_tweet = 0
                if wordsInTweet:
                    for pair in wordsInTweet:
                        wordSentimentScore = sentimentScoreFromSynonyms(pair[0], pair[1])
                        sentiment_score_tweet += wordSentimentScore
                    tupple = ({"sentiment_score": sentiment_score_tweet}, "neg")

                else:
                    tupple = ({"sentiment_score": 0}, "neg")
                negativeExamples.append(tupple)

    for tweet in timeline:
        if 'pos_tags' in tweet:
            wordsInTweet = tweet['pos_tags'] or []
            # wordsInTweet = tweet["pos_tags"]
            sentiment_score_tweet = 0
            if wordsInTweet:
                for pair in wordsInTweet:
                    wordSentimentScore = sentimentScoreFromSynonyms(pair[0], pair[1])
                    sentiment_score_tweet += wordSentimentScore
                tupple = ({"sentiment_score": sentiment_score_tweet})

            else:
                tupple = ({"sentiment_score": 0})
            testingExamples.append(tupple)
            tweetsText.append(tweet['text'])
    print "Number negative annotated", len(negativeExamples)
    print "Number positive annotated", len(positiveExamples)
    return positiveExamples + negativeExamples, testingExamples, tweetsText



##############################TIME AS MINUTES AFTER MIDNIGHT EXTRACTOR###########################3
def time_as_minutes():
    data = dataAnalysis.trainingData()
    timeline = dataAnalysis.timelineTweets
    seen = []
    negativeExamples = []
    positiveExamples = []
    testingExamples = []
    textTweet = []
    global counter
    global tupple
    for tweet in data[0]:
        if tweet["tweet_id"] not in seen:
            seen.append(tweet["tweet_id"])
            if 'min_after_midnight' in tweet:
                time_tweet = tweet['min_after_midnight'] or None
                if time_tweet:
                    tupple = ({'min_after_midnight': time_tweet}, 'pos')
                else:
                    tupple = ({'min_after_midnight': 0}, 'pos')
                positiveExamples.append(tupple)

    for tweet in data[1]:
        if tweet["tweet_id"] not in seen:
            seen.append(tweet["tweet_id"])
            if 'min_after_midnight' in tweet:
                time_tweet = tweet['min_after_midnight'] or None
                if time_tweet:
                    tupple = ({'min_after_midnight': time_tweet}, 'neg')
                else:
                    tupple = ({'min_after_midnight': 0}, 'neg')
                negativeExamples.append(tupple)

    for tweet in timeline:
        if tweet["min_after_midnight"]:
            if 'min_after_midnight' in tweet:
                textTweet.append(tweet['text'])
                time_tweet = tweet['min_after_midnight'] or None
                if time_tweet:
                    entry = ({'min_after_midnight': time_tweet})
                else:
                    entry = ({'min_after_midnight': 0})
                testingExamples.append(entry)

    print "Number negative annotated", len(negativeExamples)
    print "Number positive annotated", len(positiveExamples)
    print "Number testing tweets", len(positiveExamples)

    return positiveExamples + negativeExamples, testingExamples, textTweet



# Get all the synonyms for a word and calculate the sum of their polarity scores
def sentimentScoreFromSynonyms(word, pos):
    adverbs = ['pretty', 'fairly', 'really', 'very', 'quite']
    if mappPosTags(pos) != None:
        synsets = wn.synsets(word, pos=mappPosTags(pos))
    else:
        synsets = wn.synsets(word)
    if synsets:
        polarity_synonyms = 0
        for index in synsets:
            synonym = index.name()
            pos_score = swn.senti_synset(synonym).pos_score()
            neg_score = swn.senti_synset(synonym).neg_score()
            if pos_score > neg_score:
                polarity_synonyms += pos_score
            elif neg_score > pos_score:
                polarity_synonyms -= neg_score
        polarity_synonyms = polarity_synonyms / len(synsets)
        return polarity_synonyms
    else:
        return 0


###############NAME ENTITY EXTRACTOR#########################
def name_entities():
    data = dataAnalysis.trainingData()
    seen = []
    negativeExamples = []
    positiveExamples = []
    global tupple
    for tweet in data[0]:
        if tweet["tweet_id"] not in seen:
            seen.append(tweet["tweet_id"])
            tupple = (tweet['pod'], 'pos')
            positiveExamples.append(tupple)
            random.shuffle(positiveExamples)

    for tweet in data[1]:
        if tweet["tweet_id"] not in seen:
            seen.append(tweet["tweet_id"])
            tupple = (tweet['pod'], 'neg')
            negativeExamples.append(tupple)
            random.shuffle(negativeExamples)
    return positiveExamples + negativeExamples


####################BIGRAMS EXTRACTOR#############################
def bigramsWords(corpus):
    data = dataAnalysis.trainingData()
    words = []
    feature_vector = []
    for sentence in corpus:
        tokens = nltk.word_tokenize(sentence)
        words.append(tokens)
        bigram_measure = nltk.collocations.BigramAssocMeasures()
        finder = nltk.collocations.BigramCollocationFinder.from_words(words)
        finder.apply_freq_filter(3)
        finder.apply_word_filter(lambda w: len(w) < 3)
        finder.nbest(bigram_measure.pmi, 20)


def bigramsPosTags(corpus):
    words = []
    for sentence in corpus:
        tokens = nltk.word_tokenize(sentence)
        words.append(tokens)


def trigrams(corpus):
    return 0


###############POD EXTRACTOR#########################
def time_of_the_day():
    data = dataAnalysis.trainingData()
    seen = []
    negativeExamples = []
    positiveExamples = []
    global tupple
    for tweet in data[0]:
        if tweet["tweet_id"] not in seen:
            seen.append(tweet["tweet_id"])
            tupple = (tweet['pod'], 'pos')
            positiveExamples.append(tupple)

    for tweet in data[1]:
        if tweet["tweet_id"] not in seen:
            seen.append(tweet["tweet_id"])
            tupple = (tweet['pod'], 'neg')
            negativeExamples.append(tupple)
    return positiveExamples + negativeExamples


###############DRUGS EXTRACTOR#########################
def mentionOfDrugs():
    feature_vector = []
    data = dataAnalysis.trainingData()
    global mentions
    for tweet in data[0]:
        mentions = []
        for drug in textExtractor.getTerms(sleepDrugs):
            if drug in tweet['text']:
                mentions.append(drug)
        if mentions:
            mentions.append(len(mentions))
        else:
            mentions.append(0)
    feature_vector.append(mentions)

    for tweet in data[1]:
        mentions = []
        for drug in textExtractor.getTerms(sleepDrugs):
            if drug in tweet['text']:
                mentions.append(drug)
        if mentions:
            mentions.append(len(mentions))
        else:
            mentions.append(0)
    feature_vector.append(mentions)
    return feature_vector


def mappPosTags(x):
    if x == 'V':
        return wn.VERB
    elif x == 'N':
        return wn.NOUN
    elif x == 'A':
        return wn.ADJ
    elif x == 'R':
        return wn.ADV
    else:
        return None


def mapping(x):
    return {
        'Electronic devices, programmes or outputs': 'electronics',
        'Religious term': 'religious_terms',
        'Fear expression': 'fear_expression',
        'Psychosis-related mental health problems': 'Psychosis',
        'Swear Word': 'swear',
        'Content and location of hallucinations': 'loc_content_hallucination',
        'Physical space/location': 'physical_space',
        'Stigmatising mental health related terms': 'menthal_health_terms',
        'Own voice': 'own_voice',
    }[x]

def all_occurences(file, str):
    initial = 0
    while True:
        initial = file.find(str, initial)
        if initial == -1: return
        yield initial
        initial += len(str)
__author__ = 'mladen'
from collections import Counter

import nltk
from nltk.corpus import sentiwordnet as swn
from nltk.corpus import wordnet as wn

from TweetNLP import CMUTweetTagger
import textPreprocessing
import trainingData
from textProcessing import textExtractor

sleepDrugs = "/home/mladen/TextMiningTwitter/word_lists/sleepDrugs.txt"


def surrounding_words(iterable):
    iterator = iter(iterable)
    prev = None
    item = iterator.next()  # throws StopIteration if empty.
    for next in iterator:
        yield (prev, item, next)
        prev = item
        item = next
    yield (prev, item, None)



def pos_tags(corpus):
    feature_vectors = []
    counter = 0
    for tweet in corpus:



def bigramsWords(corpus):
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


def sentiment_score(corpus):
    # for tweet in corpus:
    polarity_score = 0
    global polarity_of_word
    adverbs = ['pretty', 'fairly', 'really', 'very', 'quite']
    tokens = textPreprocessing.tokenizeText(corpus)
    print tokens
    for index, word in enumerate(tokens):
        polarity_of_word = 0
        print word
        synset = wn.synsets(word)
        if synset:
            synset = wn.synsets(word)[0].name()
            pos_score = swn.senti_synset(synset).pos_score()
            neg_score = swn.senti_synset(synset).neg_score()
            if pos_score > neg_score:
                polarity_of_word += pos_score
                print "pos", polarity_of_word
            else:
                polarity_of_word -= neg_score
                print 'neg', polarity_of_word
            if tokens[index - 1] in adverbs:
                polarity_of_word = polarity_of_word * 0.2
            print 'word', polarity_of_word
        polarity_score += polarity_of_word
    return polarity_score
    # if negationDetection(tweet) == 0:
    #     polarity_score = polarity_score * (-1)


def mentionOfDrugs(corpus):
    feature_vector = []
    global mentions
    for tweet in corpus:
        mentions = []
        for drug in textExtractor.getTerms(sleepDrugs):
            if drug in tweet:
                mentions.append(drug)
        if mentions:
            mentions.append(len(mentions))
        else:
            mentions.append(0)
    feature_vector.append(mentions)
    return feature_vector


def time_of_the_day():
    trainingData.extractLocalTime()


def name_entities(tweet):
    tokens = textPreprocessing.tokenizeText(tweet)


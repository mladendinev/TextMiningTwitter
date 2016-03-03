__author__ = 'mladen'

import nltk.classify.util
from nltk.corpus import movie_reviews

import textProcessing.featureExtraction as features
from textProcessing import trainingData as train
from textProcessing import textPreprocessing as process

labeledData = ([(process.normaliseText(tweet), 'pos') for tweet in train.splitDataset()[0]] + [(process.normaliseText(tweet), 'neg') for tweet in train.splitDataset()[1]])
print labeledData


def compose(*functions):
    def inner(arg):
        for f in reversed(functions):
            arg = f(arg)
        return arg

    return inner


# Negative sleep tweets


def word_feats(words):
    return dict([(word, True) for word in words])


def exract_pos_features(tweet):
    pass
    # Positive sleep tweets


trainingSet = ""
validationSet = ""

negids = movie_reviews.fileids('neg')
posids = movie_reviews.fileids('pos')

negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]

negcutoff = len(negfeats) * 3 / 4
poscutoff = len(posfeats) * 3 / 4

extract_features = {0: features.pos_tags,
                    1: features.bigrams,
                    2: features.sentiment_analysis,
                    3: features.time_of_the_day,
                    4: features.bag_of_words,
                    }


def errorAnalysis(validationSet, trainingSet):
    errors = []
    for (tweet, label) in validationSet:
        classifier = nltk.NaiveBayesClassifier.train(trainingSet)
        prediciton = classifier.classify(extract_features[4]())
        if prediciton != label:
            errors.append((label, prediciton, tweet))

    for (label, prediciton, tweet) in sorted(errors):
        print('correct={:<10} guess={:<10s} tweet={:<100}'.format(label, prediciton, tweet))

#
# trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
# testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]
# print 'train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats))
#
# classifier = NaiveBayesClassifier.train(trainfeats)
# print 'accuracy:', nltk.classify.util.accuracy(classifier, testfeats)
# classifier.show_most_informative_features()

__author__ = 'mladen'
# Copyright (c) 2016 year Mladen Dinev.
# May be used free of charge.
# Selling without prior written consent prohibited.
# Obtain permission before redistributing.
# In all cases this notice must remain intact.
from sklearn.feature_extraction.text import CountVectorizer

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.feature_extraction import DictVectorizer

from textProcessing import featureExtraction as features
from textProcessing.textPreprocessing import normaliseText


def modelBagOfWords():
    featuresRawTrain, featuresRawTest = features.textTweets()
    trainingData = [element[0] for element in featuresRawTrain]
    trainingLabels = [element[1] for element in featuresRawTrain]
    testingData = [element[0] for element in featuresRawTest]
    count_vectoriser = CountVectorizer(tokenizer=normaliseText)
    modelTrainingData = count_vectoriser.fit_transform(trainingData)
    modelTestingData = count_vectoriser.transform(testingData)
    return modelTrainingData, modelTestingData, trainingLabels, count_vectoriser.get_feature_names(), featuresRawTest


def modelTfIDf():
    featuresRawTrain, featuresRawTest = features.textTweets()
    trainingData = [element[0] for element in featuresRawTrain]
    trainingLabels = [element[1] for element in featuresRawTrain]
    testingData = [element[0] for element in featuresRawTest]

    tfidfVectorizer = TfidfVectorizer(tokenizer=normaliseText)
    tf_idfTransform = tfidfVectorizer.fit_transform(trainingData)
    testing_counts = tfidfVectorizer.transform(testingData)
    return tf_idfTransform, testing_counts, trainingLabels, tfidfVectorizer.get_feature_names(), featuresRawTest


def modelPosTag():
    featuresRawTrain, featuresRawTest, tweetIds = features.pos_tags()
    return vectorizeData(featuresRawTrain, featuresRawTest, tweetIds)


def modelFreqPosTag():
    featuresRawTrain, featuresRawTest, tweetIds = features.pos_tags_frequency()
    return vectorizeData(featuresRawTrain, featuresRawTest, tweetIds)


def modelPartOfTheDay():
    featuresRawTrain, featuresRawTest, tweetIds = features.time_as_minutes()
    return vectorizeData(featuresRawTrain, featuresRawTest, tweetIds)


def modelSemanticClasses():
    featuresRawTrain, featuresRawTest, tweetIds = features.time_as_minutes()
    return vectorizeData(featuresRawTrain, featuresRawTest, tweetIds)


def vectorizeData(featuresRawTrain, featuresRawTest, tweetIds):
    vec = DictVectorizer()
    trainingData = [element[0] for element in featuresRawTrain]
    trainingLabels = [element[1] for element in featuresRawTrain]
    testingData = [element for element in featuresRawTest]
    vectorizedTrainData = vec.fit_transform(trainingData).toarray()
    vectorizeTestData = vec.transform(testingData).toarray()
    return vectorizedTrainData, vectorizeTestData, trainingLabels, vec.feature_names_, tweetIds

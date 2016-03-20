__author__ = 'mladen'
# Copyright (c) 2016 year Mladen Dinev.
# May be used free of charge.
# Selling without prior written consent prohibited.
# Obtain permission before redistributing.
# In all cases this notice must remain intact.
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import FeatureHasher

from sklearn.feature_extraction import DictVectorizer
from scipy.sparse import hstack
from textProcessing import featureExtraction as features
from textProcessing.textPreprocessing import normaliseText
from sklearn.preprocessing import Imputer


# THE MODELS FOR EACH FEATURE RESPECTIVELY

def modelBagOfWords():
    featuresRawTrain, featuresRawTest = features.textTweets()
    trainingData = [element[0] for element in featuresRawTrain]
    trainingLabels = [element[1] for element in featuresRawTrain]
    testingData = [element for element in featuresRawTest]
    count_vectoriser = CountVectorizer(tokenizer=normaliseText)
    modelTrainingData = count_vectoriser.fit_transform(trainingData)
    modelTestingData = count_vectoriser.transform(testingData)
    return modelTrainingData, modelTestingData, trainingLabels, count_vectoriser.get_feature_names(), featuresRawTest

def featuresCombined(model1,model2):
    firstModel = model1
    secondModel = model2
    # combo =  [np.hstack((model1[i],model2[i])) for i in xrange(len(model1))]
    trainingData = hstack((firstModel[0],secondModel[0]))
    testingData = hstack((firstModel[1], secondModel[1]))
    trainingLabels = firstModel[2]
    vectorizer = firstModel[3] + secondModel[3]
    rawTestTweets = firstModel[4]
    return trainingData,testingData,trainingLabels,vectorizer,rawTestTweets




def modelTfIDf():
    featuresRawTrain, featuresRawTest = features.textTweets()
    trainingData = [element[0] for element in featuresRawTrain]
    trainingLabels = [element[1] for element in featuresRawTrain]
    testingData = [element for element in featuresRawTest]

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
    featuresRawTrain, featuresRawTest, tweetIds = features.semantic_classes()
    return vectorizeData(featuresRawTrain, featuresRawTest, tweetIds)

def modelSentiment():
    featuresRawTrain, featuresRawTest, tweetIds = features.sentiment_score()
    return vectorizeData(featuresRawTrain, featuresRawTest, tweetIds)

def vectorizeData(featuresRawTrain, featuresRawTest, tweetIds):
    vec = DictVectorizer(sparse=False)
    trainingData = [element[0] for element in featuresRawTrain]
    trainingLabels = [element[1] for element in featuresRawTrain]
    testingData = [element for element in featuresRawTest]
    vectorizedTrainData = vec.fit_transform(trainingData)
    vectorizeTestData = vec.transform(testingData)


    #Use imputer to substitute the missing values with the mean of the its' collumn values
    imp = Imputer(missing_values=0, strategy='mean', axis=0)
    imp.fit(vectorizedTrainData)
    normalisedTrainingData = imp.fit_transform(vectorizedTrainData)
    normalisedTestingData = imp.transform(vectorizeTestData)
    # print len(vec.feature_names_)

    #Return the feature names after the imputer processing
    invalid_mask = np.isnan(imp.statistics_)
    valid_mask = np.logical_not(invalid_mask)
    valid_idx, = np.where(valid_mask)
    vFeature_names = np.asarray(vec.feature_names_)[valid_idx]
    print len(vFeature_names)
    return normalisedTrainingData,normalisedTestingData, trainingLabels,vFeature_names.tolist(), tweetIds



def vectorizeHasher(featuresRawTrain, featuresRawTest, tweetIds):
    hasher = FeatureHasher(input_type='dict',n_features=10)
    trainingData = [element[0] for element in featuresRawTrain]
    trainingLabels = [element[1] for element in featuresRawTrain]
    vectorizedTrainData = hasher.fit_transform(trainingData)
    testingData = [element for element in featuresRawTest]
    vectorizeTestData = hasher.transform(testingData).toarray()
    imp = Imputer(missing_values='NaN', strategy='mean', axis=0)
    removeNan = imp.fit_transform(vectorizedTrainData)
    rremovenantest = imp.transform(vectorizeTestData)
    return removeNan, rremovenantest, trainingLabels,n_nonzero_columns(removeNan),tweetIds


def n_nonzero_columns(X):
    #Returns the number of non-zero columns
    return len(np.unique(X.nonzero()[1]))
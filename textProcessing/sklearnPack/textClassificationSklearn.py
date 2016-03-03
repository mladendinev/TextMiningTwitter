__author__ = 'mladen'

import threading
import Queue
import collections

import numpy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.cross_validation import KFold
from sklearn.metrics import confusion_matrix, f1_score
from sklearn.pipeline import Pipeline
from sklearn.cross_validation import train_test_split
from sklearn.svm import SVC
from sklearn.feature_extraction import FeatureHasher
import nltk
from sklearn import ensemble

from textProcessing import trainingData
from textProcessing import textPreprocessing as process
from textProcessing import featureExtraction as features
import metricsClassifier
import random

class myThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print "Starting " + self.name
        print "Exiting " + self.name


class textClassificationSklearn():
    def __init__(self):
        self.labeledData = ([(process.normaliseText(tweet), 'pos') for tweet in trainingData.splitDataset()[0]]
                            + [(process.normaliseText(tweet), 'neg') for tweet in trainingData.splitDataset()[1]])
        random.shuffle(self.labeledData)
        self.labeledData = dict(self.labeledData)
        for x in self.labeledData:
            print x
        self.queue = Queue.Queue()

    def classifcationPosTags(self, trainingData, testingData, trainingLabels, testingLabels):

        # feature_set = features.pos_tags(dictionary.keys())
        testingFeatureSet = []
        trainingFeatureSet = []
        parameters = trainingData, testingData
        open_threads = []
        for i in range(len(parameters)):
            thread = threading.Thread(target=features.pos_tags2, args=(i, parameters[i], self.queue))
            thread.start()
            open_threads.append(thread)

        for thr in open_threads:
            thr.join()

        results = [self.queue.get() for items in xrange(len(parameters))]
        for sets in results:
            if sets[0] == 0:
                trainingFeatureSet = sets[1:]
            if sets[0] == 1:
                testingFeatureSet = sets[1:]
        # dictionary = (item for item in results if item["name"] )
        hasher = FeatureHasher(input_type='pair')
        hashedTrainFeatures = hasher.fit_transform(trainingFeatureSet)
        hashedTestFeatures = hasher.fit_transform(testingFeatureSet)
        clf = SVC()
        clf = clf.fit(hashedTrainFeatures, trainingLabels)
        clf_predict = clf.predict(hashedTestFeatures)
        metricsClassifier.classificationReport(testingLabels, clf_predict, clf)

    def countClassifier(self, trainingData, testingData, trainingLabels, testingLabels):
        count_vectoriser = CountVectorizer()
        # tf_transformer = TfidfTransformer(use_idf=False).fit_transform(trainingData)
        count_featurs = count_vectoriser.fit_transform(trainingData)
        clf = MultinomialNB().fit(count_featurs, trainingLabels)
        testing_counts = count_vectoriser.transform(testingData)
        predicted = clf.predict(testing_counts)
        metricsClassifier.classificationReport(testingLabels, predicted, clf)

    def tfIdfClassifier(self, trainingData, testingData, trainingLabels, testingLabels):
        tfidfVectorizer = TfidfVectorizer()
        tf_idfTransform = tfidfVectorizer.fit_transform(trainingData)
        # tf_transformer = TfidfTransformer(use_idf=False).fit_transform(trainingData)
        clf = MultinomialNB().fit(tf_idfTransform, trainingLabels)
        testing_counts = tfidfVectorizer.transform(testingData)
        predicted = clf.predict(testing_counts)
        metricsClassifier.classificationReport(testingLabels, predicted, clf)

    def pipeline(self):
        pipeline = Pipeline([
            ('vectorizer', CountVectorizer()),
            ('classifier', MultinomialNB())])
        return pipeline

    def validateDataset(self, trainingData, trainingLabels):
        # Predicted labels from  Cross-fold Validation
        count_vectoriser = CountVectorizer()
        # tf_transformer = TfidfTransformer(use_idf=False).fit_transform(trainingData)
        Xtrain = count_vectoriser.fit_transform(trainingData)
        predictedLabels = metricsClassifier.stratified_cv(Xtrain, trainingLabels, ensemble.RandomForestClassifier)
        showMatrix = metricsClassifier.conf_matrix(16, 12, trainingLabels, predictedLabels, "Random Forest")
        metricsClassifier.classificationReport(trainingLabels, predictedLabels, ensemble.RandomForestClassifier)
        # metricsClassifier.showImportanceOfFeatures(ensemble.RandomForestClassifier)

    def crossFoldValidation(self):
        validationSet = trainingData.splitDataset()[0]
        k_fold = KFold(len(validationSet), n_folds=10)
        scores = []
        confusion = numpy.array([[0, 0], [0, 0]])
        for train_indices, test_indices in k_fold:
            train_text = validationSet.iloc[train_indices]['text'].values
            train_label = validationSet.iloc[train_indices]['label'].values

            test_text = validationSet.iloc[test_indices]['text'].values
            test_label = validationSet.iloc[test_indices]['label'].values
            pipeline = self.pipeline()
            pipeline.fit(train_text, train_label)
            predict = pipeline.predict(test_text)
            confusion += confusion_matrix(test_label, predict)
            score = f1_score(test_label, predict, pos_label='yes')
            scores.append(score)

            print('Total sentences classified:', len(validationSet))
            print('Score:', sum(scores) / len(scores))
            print('Confusion matrix:')
            print(confusion)

            # print(metrics.classification_report(twenty_test.target, predicted,target_names=twenty_test.target_names))

    def metrics(self, labels):
        traing = collections.defaultdict(set)
        test = collections.defaultdict(set)

        for i, (prediction, label) in enumerate(labels):
            traing[label].add(i)
            test[prediction].add(i)

        pos_precision = nltk.metrics.precision(traing["pos"], test['pos'])
        pos_recall = nltk.metrics.recall(traing["pos"], test['pos'])
        neg_precision = nltk.metrics.precision(traing['neg'], test['neg'])
        neg_recall = nltk.metrics.recall(traing["neg"], test['neg'])

        return pos_precision, pos_recall, pos_recall, neg_precision, neg_recall

    def run_classifier(self):
        Xtrain, X_test, y_train, y_test = train_test_split(self.labeledData.keys(),
                                                           self.labeledData.values(),
                                                           test_size=0.33,
                                                           random_state=42)
        self.countClassifier(Xtrain, X_test, y_train, y_test)
        self.validateDataset(Xtrain, y_train)
        # print features.mentionOfDrugs(Xtrain)
        # print features.mentionOfDrugs(X_test)



if __name__ == '__main__':
    test = textClassificationSklearn()
    test.run_classifier()
# test.crossFoldValidation()

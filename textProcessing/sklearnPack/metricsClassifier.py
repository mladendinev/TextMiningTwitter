__author__ = 'mladen'

from sklearn.cross_validation import StratifiedKFold
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import datetime
import collections
from sklearn.tree import DecisionTreeClassifier
import nltk

def timestampFigure():
    currentTime = datetime.datetime.now()
    currentMonth = currentTime.month
    currentDay = currentTime.day
    currentHour = currentTime.hour
    currentMin = currentTime.minute
    currentSec = currentTime.second
    return str(currentMonth) + '-' + str(currentDay) + '-' + str(currentHour) + '-' + str(
        currentMin) + '-' + str(currentSec)

def stratified_cv(title, vec, X, y, clf_class, shuffle=True, n_folds=10, **kwargs):
    y = np.array(y)
    stratified_k_fold = StratifiedKFold(y, n_folds=n_folds, shuffle=False)
    y_pred = y.copy()
    for train, test in stratified_k_fold:
        X_train, X_test = X[train], X[test]
        y_train = y[train]
        clf = clf_class(**kwargs)
        clf.fit(X_train, y_train)
        y_pred[test] = clf.predict(X_test)
    # top10MostImportantFeautures(title, clf, vec.get_feature_names())
    return y_pred


def conf_matrix(width, height, y, predictedLabels, title):
    conf_matrix = confusion_matrix(y, predictedLabels)
    fix, ax = plt.subplots(figsize=(width, height))
    plt.suptitle('Confusion Matrix')
    plt.subplot(3, 3, 1)  # starts from 1
    plt.title(title)
    sns.heatmap(conf_matrix, annot=True, fmt='')
    plt.savefig("/home/mladen/TextMiningTwitter/textProcessing/sklearnPack/screenshots/" + timestampFigure() + title)
    plt.show()


def classificationReport(testingLabels, predictedLabels):
    print '\n Classifer Accuracy:', accuracy_score(testingLabels, predictedLabels)
    print '\n Clasification report:\n', classification_report(testingLabels, predictedLabels)


def showImportanceOfFeatures(title, classifier, feature_names):
    # Get Feature Importance from the classifier
    feature_importance = classifier.feature_importances_
    # Normalize The Features
    feature_importance = 100.0 * (feature_importance / feature_importance.max())
    sorted_idx = np.argsort(feature_importance)
    pos = np.arange(sorted_idx.shape[0]) + .5
    plt.figure(figsize=(16, 12))
    plt.barh(pos, feature_importance[sorted_idx], align='center', color='#7A68A6')
    plt.yticks(pos, np.asanyarray(feature_names)[sorted_idx])
    plt.xlabel('Feature Importance')
    plt.title('Important features')
    plt.savefig("/home/mladen/TextMiningTwitter/textProcessing/sklearnPack/screenshots/" + timestampFigure() + title)
    plt.show()


def top10MostImportantFeautures(title, classifier, feature_names):
    if isinstance(classifier, DecisionTreeClassifier):
        # Get Feature Importance from the classifier
        feature_importance = classifier.feature_importances_
        # Normalize The Features
        feature_importance = 100.0 * (feature_importance / feature_importance.max())
        sorted_idx = np.argsort(feature_importance)
        sorted_idx = sorted_idx[-10:]
        position = np.arange(sorted_idx.shape[0]) + .5
        print sorted_idx.shape[0]
        plt.figure(figsize=(16, 12))
        names = np.asanyarray(feature_names)[sorted_idx]
        print names
        # for st in names:
        #     print "Stem: %s" % st
        # print stem_buckets[st]
        plt.barh(position, feature_importance[sorted_idx], align='center', color='#7A68A6')
        plt.yticks(position, names)
        plt.xlabel('Feature Importance')
        plt.title('Top 10 Important features')
        plt.savefig("/home/mladen/TextMiningTwitter/textProcessing/sklearnPack/screenshots/" + timestampFigure() + title)
        plt.show()
    else:
        coefs_with_fns = sorted(zip(classifier.coef_[0], feature_names))
        top_features_and_names = coefs_with_fns[:-(10 + 1):-1]
        feature_coeff = np.asanyarray([element[0]for element in top_features_and_names])
        # feature_coeff =  (feature_coeff / feature_coeff.max())
        sorted_idx = np.array(feature_coeff).argsort()[::-1]
        sorted_idx2 = np.argsort(feature_coeff)
        print sorted_idx
        names = np.asanyarray([element[1] for element in top_features_and_names])

        indexes = np.arange(10)
        print feature_coeff
        print indexes
        print names
        # sorted_idx = np.argsort(coefs_with_fns[:-(10 + 1):-1])
        position = np.arange(feature_coeff.shape[0]) + .5
        plt.figure(figsize=(16, 12))
        top = zip(coefs_with_fns[:10], coefs_with_fns[:-(10 + 1):-1])
        for (coef_1, fn_1), (coef_2, fn_2) in top:
            print "\t%.4f\t%-15s\t\t%.4f\t%-15s" % (coef_1, fn_1, coef_2, fn_2)
        plt.barh(position, feature_coeff[sorted_idx2], align='center', color='#7A68A6')
        plt.yticks(position, names)
        plt.xlabel('Importance')
        plt.ylabel('Feature names')
        plt.title('Top 10 Important features')
        plt.show()

def metrics(labels):
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


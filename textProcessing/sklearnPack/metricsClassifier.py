__author__ = 'mladen'

from sklearn.cross_validation import StratifiedKFold
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report



def stratified_cv(X, y, clf_class, shuffle=True, n_folds=10, **kwargs):
    y = np.array(y)
    stratified_k_fold = StratifiedKFold(y, n_folds=n_folds, shuffle=shuffle)
    y_pred = y.copy()
    for train, test in stratified_k_fold:
        X_train, X_test = X[train], X[test]
        y_train = y[train]
        clf = clf_class(**kwargs)
        clf.fit(X_train, y_train)
        y_pred[test] = clf.predict(X_test)
    return y_pred


def conf_matrix(width, height, y,predictedLabels, Title):
    conf_matrix = confusion_matrix(y,predictedLabels)
    print conf_matrix
    fix, ax = plt.subplots(figsize=(width, height))
    plt.suptitle('Confusion Matrix')
    plt.subplot(3, 3, 1)  # starts from 1
    plt.title(Title)
    sns.heatmap(conf_matrix, annot=True, fmt='')
    plt.show()



def classificationReport(testingLabels, predictedLabels, clf):
    print '\n Classifer Accuracy: \n', accuracy_score(testingLabels, predictedLabels)
    print '\n Clasification report:\n', classification_report(testingLabels, predictedLabels)


def showImportanceOfFeatures(classifier, feature_names):
    # Get Feature Importance from the classifier
    feature_importance = classifier.feature_importances_
    # Normalize The Features
    feature_importance = 100.0 * (feature_importance / feature_importance.max())
    sorted_idx = np.argsort(feature_importance)
    pos = np.arange(sorted_idx.shape[0]) + .5
    plt.figure(figsize=(16, 12))
    plt.barh(pos, feature_importance[sorted_idx], align='center', color='#7A68A6')
    plt.yticks(pos, np.asanyarray(feature_names)[sorted_idx])
    plt.xlabel('Relative Importance')
    plt.title('Variable Importance')
    plt.show()

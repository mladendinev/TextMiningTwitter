__author__ = 'mladen'

import threading

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.cross_validation import train_test_split
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.feature_extraction import DictVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_selection import VarianceThreshold
from sklearn.svm import SVC
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.grid_search import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import Imputer
from textProcessing import featureExtraction as features
import metricsClassifier
from textProcessing.textPreprocessing import normaliseText


class TextStats(BaseEstimator, TransformerMixin):
    def fit(self, x, y=None):
        return self

    def transform(self, posts):
        return [{'length': len(text),
                 'num_sentences': text.count('.')}
                for text in posts]


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
    def __init__(self, selectFeature):
        option = {0: features.pos_tags,
                  1: features.pos_tags_frequency,
                  2: features.time_as_minutes,
                  3: features.mentionOfDrugs,
                  4: features.textTweets,
                  5: features.textTweets,
                  6: features.semantic_classes,
                  7: features.sentiment_score,
                  }

        self.choice = selectFeature
        # print len(option[selectFeature]()[0])
        # print len(option[selectFeature]()[1])
        self.labeledData = option[selectFeature]()[0]

    def combineFeatures(self, training, testingData, trainingLabels, testingLabels):
        pipeline = Pipeline([
            ('vect', CountVectorizer()),
            ('tfidf', TfidfTransformer()),
            ('clf', MultinomialNB()),
        ])
        pipeline.fit(training, trainingLabels)
        metricsClassifier.classificationReport(testingLabels, pipeline.predict(testingData))
        showMatrix = metricsClassifier.conf_matrix(16, 12, testingLabels, pipeline.predict(testingData), "Bag-of-words")

    def countClassifier(self, trainingData, testingData, trainingLabels, testingLabels):
        count_vectoriser = CountVectorizer(tokenizer=normaliseText)
        count_featurs = count_vectoriser.fit_transform(trainingData)
        # clf = SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, n_iter=5, random_state=42).fit(count_featurs, trainingLabels)
        clf = MultinomialNB().fit(count_featurs, trainingLabels)
        testing_counts = count_vectoriser.transform(testingData)
        predicted = clf.predict(testing_counts)
        metricsClassifier.classificationReport(testingLabels, predicted)
        showMatrix = metricsClassifier.conf_matrix(16, 12, testingLabels, predicted, "Bag-of-words")
        # importance = metricsClassifier.showImportanceOfFeatures("Pos-Tags",clf,count_vectoriser.get_feature_names())
        metricsClassifier.top10MostImportantFeautures("Bag-of-words", clf, count_vectoriser.get_feature_names())

    def tfIdfClassifier(self, trainingData, testingData, trainingLabels, testingLabels):
        tfidfVectorizer = TfidfVectorizer()
        tf_idfTransform = tfidfVectorizer.fit_transform(trainingData)
        ch2 = SelectKBest(chi2, k='all')
        X_train_features = ch2.fit_transform(tf_idfTransform, trainingLabels)
        clf = MultinomialNB().fit(X_train_features, trainingLabels)
        testing_counts = tfidfVectorizer.transform(testingData)
        predicted = clf.predict(testing_counts)
        metricsClassifier.classificationReport(testingLabels, predicted)
        showMatrix = metricsClassifier.conf_matrix(16, 12, testingLabels, predicted, "TF-IDF")
        metricsClassifier.top10MostImportantFeautures("Bag-of-words", clf, tfidfVectorizer.get_feature_names())

    def classificaitonPosTags(self, trainingData, testingData, trainingLabels, testingLabels):
        vec = DictVectorizer()
        # print trainingData
        vectorized = vec.fit_transform(trainingData + testingData)
        vectorizeTestData = vec.transform(testingData)
        # clf = SVC()
        # clf = clf.fit(hashedTrainFeatures, trainingLabels)
        # clf_predict = clf.predict(hashedTestFeatures)
        # metricsClassifier.classificationReport(testingLabels, clf_predict, clf)

        clf = DecisionTreeClassifier()
        clf = clf.fit(vectorized.toarray(), trainingLabels + testingLabels)
        #
        # clf_predict = clf.predict(vectorizeTestData.toarray())
        # metricsClassifier.classificationReport(testingLabels, clf_predict)
        # predictedLabels = metricsClassifier.stratified_cv("Pos-Tags", vec, vectorized, trainingLabels,
        #                                                   DecisionTreeClassifier)
        # showMatrix = metricsClassifier.conf_matrix(16, 12, testingLabels, clf_predict, "Pos-Tags")
        # metricsClassifier.showImportanceOfFeatures("Pos-Tags",clf,vec.feature_names_)
        metricsClassifier.top10MostImportantFeautures("Pos-Tags", clf, vec.feature_names_)

    def classifcationFreqPosTags(self, trainingData, testingData, trainingLabels, testingLabels):
        vec = DictVectorizer()
        vectorized = vec.fit_transform(trainingData)
        vectorizeTestData = vec.transform(testingData)
        clf = DecisionTreeClassifier()
        clf = clf.fit(vectorized.toarray(), trainingLabels)
        clf_predict = clf.predict(vectorizeTestData.toarray())
        metricsClassifier.classificationReport(testingLabels, clf_predict)
        showMatrix = metricsClassifier.conf_matrix(16, 12, testingLabels, clf_predict, "Freq-Pos-Tags")
        metricsClassifier.top10MostImportantFeautures("Freq-Pos-Tags", clf, vec.feature_names_)

    def semantic_classes(self, trainingData, testingData, trainingLabels, testingLabels):
        # chain = itertools.chain(*trainingData)
        # print trainingData
        # hahsher = FeatureHasher(input_type='string')
        vec = DictVectorizer()

        feature_set = vec.fit_transform(trainingData).toarray()
        clf = RandomForestClassifier(n_estimators=1000)
        # tf_transformer = TfidfTransformer(use_idf=False).fit_transform(trainingData)
        clf = clf.fit(feature_set, trainingLabels)
        testing_counts = vec.transform(testingData).toarray()
        predicted = clf.predict(testing_counts)
        metricsClassifier.classificationReport(testingLabels, predicted, )
        showMatrix = metricsClassifier.conf_matrix(16, 12, testingLabels, predicted, "Semantic_Classes")
        metricsClassifier.top10MostImportantFeautures("Semantic_Classes", clf, vec.feature_names_)

    def svmClassifer(self, xtrain, xtest, ytrain, ytest, clf_class, **kwargs):
        vec = DictVectorizer()
        vectorizedTrainingData = vec.fit_transform(xtrain).toarray()
        vectorizeTestData = vec.transform(xtest).toarray()

        clf = clf_class(**kwargs)
        clf.fit(vectorizedTrainingData, ytrain)
        predicted = clf.predict(vectorizeTestData)
        metricsClassifier.classificationReport(ytest, predicted)

    def validateDataset(self, trainingData, trainingLabels):
        # vec = CountVectorizer(tokenizer=normaliseText)
        vec = TfidfVectorizer(tokenizer=normaliseText)
        # vec = DictVectorizer()
        vectorizedTrainingData = vec.fit_transform(trainingData).toarray()
        # sel = VarianceThreshold(threshold=(.6 * (1 - .6)))
        for classifier in (DecisionTreeClassifier, RandomForestClassifier, MultinomialNB):
            # SVC,kernel='linear',C=1
            predictedLabels = metricsClassifier.stratified_cv("Decision Tree", vec, vectorizedTrainingData,
                                                              trainingLabels, SVC, kernel='linear', C=1)
            showMatrix = metricsClassifier.conf_matrix(16, 12, trainingLabels, predictedLabels,
                                                       "DecisionTreeClassifier")
            # metricsClassifier.top10MostImportantFeautures("Semantic_Classes", DecisionTreeClassifier, vec.feature_names_)
            metricsClassifier.classificationReport(trainingLabels, predictedLabels)
            break

    def validateDataset2(self, trainingData, testing, trainingLabels):
        # vec = CountVectorizer(tokenizer=normaliseText)
        vec = DictVectorizer()

        vectorizedTrainData = vec.fit_transform(trainingData)
        vectorizeTestData = vec.transform(testing)


        # Use imputer to substitute the missing values with the mean of the its' collumn values
        imp = Imputer(missing_values=0, strategy='mean', axis=0)
        imp.fit(vectorizedTrainData)
        trialData = imp.fit_transform(vectorizedTrainData)
        trialTest = imp.transform(vectorizeTestData)
        # print len(vec.feature_names_)


        # Return only the non-nan feature names
        invalid_mask = np.isnan(imp.statistics_)
        valid_mask = np.logical_not(invalid_mask)
        valid_idx, = np.where(valid_mask)
        vFeature_names = np.asarray(vec.feature_names_)[valid_idx]

        vectorizedTrainingData = vec.fit_transform(trainingData).toarray()
        # sel = VarianceThreshold(threshold=(.6 * (1 - .6)))

        for classifier in (DecisionTreeClassifier, RandomForestClassifier, MultinomialNB):
            predictedLabels = metricsClassifier.stratified_cv("Decision Tree", vec, trialData,
                                                              trainingLabels, SVC, kernel='linear', C=1)
            showMatrix = metricsClassifier.conf_matrix(16, 12, trainingLabels, predictedLabels,
                                                       "DecisionTreeClassifier")

            # metricsClassifier.top10MostImportantFeautures("Semantic_Classes", DecisionTreeClassifier, vec.feature_names_)
            metricsClassifier.classificationReport(trainingLabels, predictedLabels)
            break

    def run_classifier(self):
        Xtrain, Xtest, y_train, y_test = train_test_split([element[0] for element in self.labeledData],
                                                           [element[1] for element in self.labeledData],
                                                           test_size=0.33,
                                                           random_state=43)
        # self.tuneParameters(Xtrain, Xtest, y_train, y_test)
        # if self.choice == 0:
        #     self.classificaitonPosTags(Xtrain, Xtest, y_train, y_test)
        # elif self.choice == 1:
        #     self.classifcationFreqPosTags(Xtrain, Xtest, y_train, y_test)
        # elif self.choice == 4:
        #     self.countClassifier(Xtrain, Xtest, y_train, y_test)
        # elif self.choice == 5:
        #     self.tfIdfClassifier(Xtrain, Xtest, y_train, y_test)
        # elif self.choice == 6:
        #     self.semantic_classes(Xtrain, Xtest, y_train, y_test)
        # elif self.choice == 7:
        #     self.classificaitonPosTags(Xtrain, Xtest, y_train, y_test)
        # else:
        #     raise ValueError('Classifier does not exists')
        #

        # pipe = Pipeline([
        #     ('vectorizer', DictVectorizer()),
        #     ('classifier', DecisionTreeClassifier())])
        #
        # classifier = pipe.fit_transform(Xtrain,y_train)
        # predicted = classifier.predict(Xtest)
        # metricsClassifier.classificationReport(y_test, predicted)
        # showMatrix = metricsClassifier.conf_matrix(16, 12, y_test, predicted, "Freq-Pos-Tags")
        # metricsClassifier.top10MostImportantFeautures("Freq-Pos-Tags", pipe.named_steps['vectorizer'], pipe.named_steps['vectorizer'].feature_names_)


        self.validateDataset2(Xtrain,Xtest,y_train)
        #


if __name__ == '__main__':
    # option = {0: features.pos_tags,
    #           1: features.pos_tags_frequency,
    #           2: features.time_as_minutes,
    #           3: features.mentionOfDrugs,
    #           4: features.textTweets,
    #           5: features.textTweets,
    #           6: features.semantic_classes,
    #           7: features.sentiment_score(),
    test = textClassificationSklearn(7)
    test.run_classifier()
# test.crossFoldValidation()

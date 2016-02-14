__author__ = 'mladen'

from database import dbOperations
from pandas import concat
import numpy
from pandas import DataFrame
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.cross_validation import KFold
from sklearn.metrics import confusion_matrix, f1_score
from sklearn.pipeline import Pipeline



class textClassificationNltk():

    def getData(self):
        dbHelper = dbOperations.dbOperations("local")

        # Positive sleep tweets
        sleepRelated = dbHelper.returnSleepTweets("sleepTweetsTest", "sleepRelated", "yes")

        # Negative sleep tweets
        nonSleepRelated = dbHelper.returnSleepTweets("sleepTweetsTest", "sleepRelated", "no")

        concatenateList = sleepRelated + nonSleepRelated

        trainingdata = DataFrame(concatenateList)
        return trainingdata

    def classification(self):
        trainingdata = self.getData()
        trainingdata = trainingdata.reindex(numpy.random.permutation(trainingdata.index))

        count_vectorizer = CountVectorizer()
        counts = count_vectorizer.fit_transform(trainingdata['text'].values)

        classifier = MultinomialNB()
        targets = trainingdata['label'].values
        classifier.fit(counts, targets)

        examples = ['I am so tired I want to sleep', "I'm going to attend the Linux users group tomorrow."]
        example_counts = count_vectorizer.transform(examples)
        predictions = classifier.predict(example_counts)
        print predictions


    def pipeline(self):
        pipeline = Pipeline([
            ('vectorizer',  CountVectorizer()),
            ('classifier',  MultinomialNB()) ])
        return pipeline

    def crossFoldValidation(self):
        validationSet = self.getData()
        k_fold = KFold(len(validationSet), n_folds=10)
        scores = []
        confusion = numpy.array([[0, 0], [0, 0]])
        for train_indices, test_indices in k_fold:
            train_text = validationSet.iloc[train_indices]['text'].values
            train_label = validationSet.iloc[train_indices]['label'].values

            test_text = validationSet.iloc[test_indices]['text'].values
            test_label = validationSet.iloc[test_indices]['label'].values
            pipeline = self.pipeline()
            pipeline.fit(train_text,train_label)
            predict = pipeline.predict(test_text)
            confusion += confusion_matrix(test_label,predict)
            score = f1_score(test_label, predict, pos_label='yes')
            scores.append(score)

            print('Total sentences classified:', len(validationSet))
            print('Score:', sum(scores)/len(scores))
            print('Confusion matrix:')
            print(confusion)

            # print(metrics.classification_report(twenty_test.target, predicted,target_names=twenty_test.target_names))
if __name__ == '__main__':
    test = textClassificationNltk()
    # test.classification()
    test.crossFoldValidation()

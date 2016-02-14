__author__ = 'mladen'
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews


class testSentimentAnalysis(object):
    def __init__(self):
        self.negids = movie_reviews.fileids('neg')
        self.posids = movie_reviews.fileids('pos')

        self.negfeats = [(self.wordAsFeauture(movie_reviews.words(fileids=[f])), 'neg') for f in self.negids]
        self.posfeats = [(self.wordAsFeauture(movie_reviews.words(fileids=[f])), 'pos') for f in self.posids]

        self.negcutoff = len(self.negfeats) * 3 / 4
        self.poscutoff = len(self.posfeats) * 3 / 4

    def wordAsFeauture(self, tweet):
        return dict([word, True] for word in tweet)


if __name__ == "__main__":
        sentiment =  testSentimentAnalysis()
        trainfeats = sentiment.negfeats[:sentiment.negcutoff] + sentiment.posfeats[:sentiment.poscutoff]
        testfeats = sentiment.negfeats[sentiment.negcutoff:] + sentiment.posfeats[sentiment.poscutoff:]
        print 'train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats))

        classifier = NaiveBayesClassifier.train(trainfeats)
        print 'accuracy:', nltk.classify.util.accuracy(classifier, testfeats)
        classifier.show_most_informative_features()
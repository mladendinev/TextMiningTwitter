__author__ = 'mladen'

from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

class sleepTextClassifier():
    categories= ['alt.atheism', 'soc.religion.christian', 'comp.graphics', 'sci.med']
    twenty_train =fetch_20newsgroups(subset='train', categories=categories, shuffle=True, random_state=42)
    count_vect = CountVectorizer()
    tfidf_transformer= TfidfTransformer()

    def featureExtraction(self):

        X_train_counts = self.count_vect.fit_transform(self.twenty_train.data)
        tfidf_train = self.tfidf_transformer.fit_transform(X_train_counts)
        return tfidf_train

    def trainingClassifier(self):
        trainingVector = self.featureExtraction()
        clf = MultinomialNB().fit(trainingVector, self.twenty_train.target)
        docs_new = ['God is love', 'OpenGL on the GPU is fast']
        X_new_counts = self.count_vect.transform(docs_new)
        X_new_tfidf = self.tfidf_transformer.transform(X_new_counts)
        predicted = clf.predict(X_new_tfidf)
        for doc, category in zip(docs_new, predicted):
            print('%r => %s' % (doc, self.twenty_train.target_names[category]))

if __name__ == "__main__":
    import logging
    logging.basicConfig()
    textClassifier1 = sleepTextClassifier()
    textClassifier1.trainingClassifier()

__author__ = 'mladen'

import nltk, string
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from collections import Counter
import tweetsOperations as ops
import re
from sklearn.metrics.pairwise import linear_kernel
import math
from history import CMUTweetTagger
from nltk.corpus import sentiwordnet
from nltk.corpus import wordnet as wn

stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
stopwords = stopwords.words('english')

def posTagging(listTweets):
    results = []
    for tweet in listTweets:
        results.append(CMUTweetTagger.runtagger_parse([tweet]))
    return results

def extractEntities(listTweets):
    results = []
    for tweet in listTweets:
        # tweet = tweet.encode('utf-8')
        tweet = tokenizeText(tweet)
        tag = nltk.pos_tag(tweet)
        results.append(nltk.chunk.ne_chunk(tag))
    return results

def wordContext(text):
    text = sentiwordnet.senti_synset('')

def tf(word, blob):
    return blob.words.count(word) / len(blob.words)


def n_containing(word, bloblist):
   return sum(1 for blob in bloblist if word in blob)

def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)


def frequencyCounter(text):
    # remove stopwords
    words = tokenizeText(text)
    words = [word for word in words if word not in stopwords]
    words = Counter(words)
    return words


def tokenizeText(text):
    text = ops.analyseText(text)
    text = text.lower()
    punct = re.compile(r'([^A-Za-z0-9 ])')
    punct.sub("", text)
    tokens = nltk.word_tokenize(text)
    return tokens


def stemming(text):
    stem1 = []
    tokens = tokenizeText(text)
    for items in tokens:
        stem1.append(stemmer.stem(items))
    return stem1


def tfidfFunc():
    tokenDict = {}
    tokenDict[0] = "I fired a cannon"
    tokenDict[1] = "I fired a rocket"
    vectorizer = TfidfVectorizer(tokenizer=stemming, stop_words=stopwords)

    tfidf = vectorizer.fit_transform(tokenDict.values())

    cosine_similarities = linear_kernel(tfidf[0:1], tfidf).flatten()
    print vectorizer.get_feature_names()

    return tfidf


    # '''remove punctuation, lowercase, stem'''
    # def normalize(text):
    #     return stemming(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))
    #
    # vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')
    #
    # def cosine_sim(text1, text2):
    #     tfidf = vectorizer.fit_transform([text1, text2])
    #     return ((tfidf * tfidf.T).A)[0,1]
    #
    #
    # print cosine_sim('a little bird', 'a little bird')
    # print cosine_sim('a little bird', 'a little bird chirps')
    # print cosine_sim('a little bird', 'a big dog barks')

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

from collections import defaultdict

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
    # text = ops.analyseText(text)
    # text = text.lower()
    # punct = re.compile(r'([^A-Za-z0-9 ])')
    # punct.sub("", text)
    tokens = nltk.word_tokenize(text)
    stemmedtokens = stemming(tokens)
    return stemmedtokens


def stemming(text):
    stem1 = []
    for items in text:
        stem1.append(stemmer.stem(items))
    return stem1

def removePunctuation(text):
    filtered =  text.translate(remove_punctuation_map)
    return filtered



def testScit():

    filterList = ["schizophreniform","schizo","affective","psychosis","delusional", "disorder","shared","psychotic","foile","a","deux",
                  "induced","psychosis","psychotic", "disorder","schiz"]

    tweets = defaultdict(list)
    with open("diagnostic_tweets",'r') as f:
        for count, lines in enumerate(f.readlines()):
            # if any(word in lines for word in filterList):
            newline = ' '.join(lines.split())
            processed_tweet = ops.analyseText(newline)
            remove = '|'.join(filterList)
            regex = re.compile(r'\b('+remove+r')\b', flags=re.IGNORECASE)
            out = regex.sub("", processed_tweet)

            # newline = ' '.join(lines.split())
            tweets[count].append(out)

    for tweet_no, tweet in tweets.iteritems():
            tweets[tweet_no] = ''.join(tweet)

    corpus = []
    for id, tweet in sorted(tweets.iteritems(), key=lambda t:int(t[0])):
        corpus.append(tweet)


    tf = TfidfVectorizer(analyzer='word', ngram_range=(1,3), min_df = 0, stop_words = 'english')
    tf_idf = tf.fit_transform(corpus)
    feature_names = tf.get_feature_names()

    dense = tf_idf.todense()
    test_tweet = dense[1].tolist()[0]
    phrase_scores = [pair for pair in zip(range(0, len(test_tweet)), test_tweet) if pair[1] > 0]

    sorted_phrase_scores = sorted(phrase_scores, key=lambda t: t[1] * -1)
    for phrase, score in [(feature_names[word_id], score) for (word_id, score) in sorted_phrase_scores][:20]:
        print('{0: <20} {1}'.format(phrase, score))



    # print corpus
    #
    #
    #
    #






















def tfidfFunc():
    # tokenDict = {}
    # tokenDict[0] = "I fired a cannon"
    # tokenDict[1] = "I fired a rocket"
    dict_tokens=[]
    with open("diagnostic_tweets",'r') as f:
        for lines in f.readlines():
            newline = ' '.join(lines.split())

            process_tweet = ops.analyseText(newline)
            # print process_tweet
            dict_tokens.append(process_tweet)
        vectorizer = TfidfVectorizer(tokenizer=tokenizeText, stop_words=stopwords)

        tfidf = vectorizer.fit_transform(dict_tokens)
            # print tfidf[0:1]
            # str = 'this sentence has unseen text such as computer but also king lord juliet'
            # response = vectorizer.transform([str])
            # print response
        feature_names = vectorizer.get_feature_names()
        print feature_names
            # for col in response.nonzero()[1]:
            #     print feature_names[col], ' - ', response[0, col]


        cosine_similarities = linear_kernel(tfidf[0:1], tfidf).flatten()
        related_docs_indices = cosine_similarities.argsort()[:-5:-1]
        similiarities = cosine_similarities[related_docs_indices]
        print similiarities
        print related_docs_indices
        print dict_tokens[11]
                # print cosine_similarities

            # nt vectorizer.get_feature_names()


        # def cosine_sim(text1, text2):
        #     tfidf = vectorizer.fit_transform([text1, text2])
        #     return ((tfidf * tfidf.T).A)[0,1]
        #
        #
        # print cosine_sim('a little bird', 'a little bird')
        # print cosine_sim('a little bird', 'a little bird chirps')
        # print cosine_sim('a little bird', 'a big dog barks')

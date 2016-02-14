# __author__ = 'mladen'

import Levenshtein
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import TweetTokenizer
import langid
from nltk.parse import stanford
from nltk.parse import dependencygraph
from nltk import wordpunct_tokenize
from nltk.corpus import stopwords
import os
from enchant.checker import SpellChecker
from enchant.tokenize import EmailFilter, URLFilter
import re
from unidecode import unidecode
from collections import Counter
from history import CMUTweetTagger
import nltk
# from enchant.checker.wxSpellCheckerDialog import wxSpellCheckerDialog
import textExtractor
import string
from nltk.stem import WordNetLemmatizer

# import edu.stanford.nlp.trees.semgraph.SemanticGraph

stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
stopwords = stopwords.words('english')


def lexical_diversity(text):
    return len(set(text)) / len(text)


def content_fraction(text):
    stopwordsInCorpus = stopwords.words('english')
    content = [w for w in text if w.lower() not in stopwordsInCorpus]
    return len(content) / len(text)


def detectLanguage(tweet):
    tupple = langid.classify(tweet)
    language = tupple[0]
    if language == "en":
        return True
    else:
        return False


def retweeeted(tweet):
    if "RT" in tweet:
        return True
    else:
        return False


def containLinks(tweet):
    if "https://" in tweet or "http://" in tweet:
        return True
    else:
        return False


validators = {"Retweet": retweeeted,
              "Links": containLinks,
              "Language": detectLanguage}


def utf8(s):
    if isinstance(s, str):
        return unicode(s, 'utf-8')
        return s


def clearpunct(s):
    tokenizer = RegexpTokenizer(r'\w+')
    return " ".join(tokenizer.tokenize(s))


def strclean(s):
    s = utf8(s)
    return clearpunct(s.lower())


#
# def checkSpelling(tweet):
#     app = wx.PySimpleApp()
#     dlg = wxSpellCheckerDialog(None,-1,"")
#     checker = SpellChecker("en_US", tweet)
#     dlg.SetSpellChecker(checker)
#     dlg.Show()
#     app.MainLoop()
#     checker.set_text(tweet)
# tokenized_tweet = tknzr.tokenize(tweet)

# for err in checker:
#     print "Spelling mistakes", err.word
#     print "Suggested words", checker.suggest(err.word)
#


def removeHashTag(tweet):
    for words in tweet.split():
        if words.startsWith('#'):
            words.replace('%')


def objectRemoval(tweet):
    # Replace unnecessary string "objects" from the tweets
    tweet = re.sub('(http://([^\s]+))', '', tweet)
    tweet = re.sub('(https://([^\s]+))', '', tweet)
    tweet = re.sub(r'RT\s+(@[^\s]+)\s*\:?', '', tweet)
    tweet = re.sub(r'(@[^\s]+)', '', tweet)
    tweet = re.sub(r'(#([^\s]+))', '', tweet)

    # Fixing extra whitespaces before and after words
    tweet = tweet.strip()
    return tweet


def frequencyCounter(text):
    # remove stopwords
    words = tokenizeText(text)
    words = [word for word in words if word not in stopwords]
    words = Counter(words)
    return words


def remove_special_unicode(text):
    if isinstance(text, str):
        text = text.decode("utf-8", "ignore")
    return unidecode(text).replace("[?]", "")


def analyseText(tweet):
    text = ''
    # text = remove_emoji(tweet)
    text = objectRemoval(tweet)
    return text


# Remove emoji from tweets
def remove_emoji(tweet):
    if isinstance(tweet, str):
        tweet = tweet.decode("utf-8", "ignore")
    try:
        highpoints = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        highpoints = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')

    tweet = highpoints.sub(u'', tweet)
    return tweet


# Tag each word as part of setence
def posTagging(listTweets):
    results = []
    for tweet in listTweets:
        results.append(CMUTweetTagger.runtagger_parse([tweet]))
    return results


def tokenizeText(text):
    # punct = re.compile(r'([^A-Za-z0-9 ])')
    # punct.sub("", text)
    tokens = nltk.word_tokenize(text)
    return tokens


# Method using the Porter stemer for tagging each tweet
def stemming(text):
    stem = []
    for items in tokenizeText(text):
        stem.append(stemmer.stem(items))
    return ' '.join(stem)


# Removing the punctuation
def removePunctuation(text):
    filtered = text.translate(remove_punctuation_map)
    return filtered


# Lemamtization
def lemmatization(text):
    lemmatizer = nltk.WordNetLemmatizer()
    lemmas = [lemmatizer.lemmatize(token) for token in tokenizeText(text)]
    return ' '.join(lemmas)

def replaceAbbreviation(tweet):
    tweet = tweet.lower()
    words = tweet.split()
    abbreviationDict = textExtractor.getAbbreviations()
    for token in words:
        if token in abbreviationDict.keys():
            print "Found Abbreviation"
            tweet = tweet.replace(token, abbreviationDict.get(token))
    return tweet
# def dependencyTree(self):
#     dependencies = self.parser.parseToStanfordDependencies("Ivan is a good guy.")
#     return dependencies

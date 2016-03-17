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
from nltk.tag.stanford import StanfordNERTagger
from TweetNLP.twokenize import tokenizeRawTweetText


# from enchant.checker.wxSpellCheckerDialog import wxSpellCheckerDialog
import textExtractor
import string
from nltk.stem import WordNetLemmatizer

# import edu.stanford.nlp.trees.semgraph.SemanticGraph

stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
cacheStopwords = stopwords.words('english')


def duplicates(seq):
    seen = set()
    seen_add = seen.add
    seen_twice = set(x for x in seq if x in seen or seen_add(x))
    # turn the set into a list (as requested)
    return list(seen_twice)


def lexical_diversity(text):
    return len(set(text)) / len(text)


def content_fraction(text):
    content = [w for w in text if w.lower() not in cacheStopwords]
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
    words = removeStopwords(text)
    words = Counter(words)
    return words


def remove_special_unicode(text):
    if isinstance(text, str):
        text = text.decode("utf-8", "ignore")
    return unidecode(text).replace("[?]", "")


def removeStopwords(text):
    text = tokenizeText(text)
    words = [word for word in text if word not in cacheStopwords]
    return ' '.join(words)


def analyseText(tweet):
    tweet = tweet.replace("\n",' ')
    tweet = tweet.replace("&amp", "")
    emojiRemove = remove_emoji(tweet)
    objRemove = objectRemoval(emojiRemove)
    return objRemove


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
def posTagging(text):
    results = CMUTweetTagger.runtagger_parse([text])
    return results


def tokenizeText(text):
    # punct = re.compile(r'([^A-Za-z0-9 ])')
    # punct.sub("", text)
    tokens = tokenizeRawTweetText(text)
    return tokens


# Method using the Porter stemer for tagging each tweet
def stemming(text):
    stem = []
    for items in text:
        stem.append(stemmer.stem(items))
    return ' '.join(stem)


# Removing the punctuation
def removePunctuation(text):
    out = text.translate(remove_punctuation_map)
    return out


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
            tweet = tweet.replace(token, abbreviationDict.get(token))
    return tweet


def compose(*functions):
    def inner(arg):
        for f in reversed(functions):
            arg = f(arg)
        return arg

    return inner


stem_buckets = {}
def normaliseText(tweet):
    global stem_buckets
    tweet = tweet.lower()
    tweet = tweet.replace("&amp", "")
    filterTweet = analyseText(tweet)
    tweet = replaceAbbreviation(filterTweet)
    # noPunct = removePunctuation(filterTweet)
    tokens = tokenizeText(filterTweet)
    text = []
    for token in tokens:
        if token not in cacheStopwords and token not in string.punctuation:
            st = stemmer.stem(token)
            if st not in stem_buckets:
                stem_buckets[st] = set()
            stem_buckets[st].add(token)
            text.append(st)
    # tweet = ' '.join(text)
    return text


def unlabelled_entity_names(text):
    filterTweet = analyseText(text)
    text = removePunctuation(filterTweet)
    data = nltk.word_tokenize(text)
    tagged = nltk.pos_tag(data)
    namedEnt = nltk.ne_chunk(tagged, binary=True)
    entity = []
    for subtree in namedEnt.subtrees(filter=lambda x: x.label() == 'NE'):
        entity.append(subtree.leaves())
    return entity


def tagg_tweet(text):
    text = removePunctuation(text)
    filterTweet = analyseText(text)
    st = StanfordNERTagger(
        '/home/mladen/TextMiningTwitter/stanford-ner-2015-01-30/classifiers/english.all.7class.distsim.crf.ser.gz',
        '/home/mladen/TextMiningTwitter/stanford-ner-2015-01-30/stanford-ner.jar',
        encoding='utf-8')
    tokenized_text = nltk.word_tokenize(filterTweet)
    classified_text = st.tag(tokenized_text)
    return classified_text


def label_entity(sent):
    chunks = []
    first_chunk = []

    for token, tag in sent:
        if tag != "O":
            first_chunk.append((token, tag))
        else:
            if first_chunk:
                chunks.append(first_chunk)
                first_chunk = []
    if first_chunk:
        chunks.append(first_chunk)
    return chunks

def semanticNormalisation(listData):
    normalised = []
    for element in listData:
        element = element.lower()
        normalised.append(element)
    return normalised

def normSentiment(tweet):
    #emojiRemove = remove_emoji(tweet)
    tweet = tweet.replace("\n",' ')
    tweet = tweet.replace("&amp", "")
    tweet = replaceAbbreviation(tweet)
    return tweet


# def dependencyTree(self):
#     dependencies = self.parser.parseToStanfordDependencies("Ivan is a good guy.")
#     return dependencies

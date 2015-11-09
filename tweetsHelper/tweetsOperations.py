# __author__ = 'mladen'

import Levenshtein
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import TweetTokenizer
import langid
from nltk.parse import stanford
from nltk import wordpunct_tokenize
from nltk.corpus import stopwords
import os
from enchant.checker import SpellChecker
from enchant.tokenize import EmailFilter, URLFilter
import re
from unidecode import unidecode


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


def checkSpelling(tweet):
    checker = SpellChecker("en_US", filters=[EmailFilter, URLFilter])
    tknzr = TweetTokenizer()
    checker.set_text(tweet)
    lengthOfText = len(tweet)
    tokenized_tweet = tknzr.tokenize(tweet)

    for word in tokenized_tweet:
        print "Spelling mistakes", word

#
# def removeHashTag(tweet):
#     for words in tweet.split()
#         if words.startsWith('#')
#             words.replace('%')


def objectRemoval(tweet):
    tweet = re.sub('(http://([^\s]+))', '', tweet)
    tweet = re.sub('(https://([^\s]+))', '', tweet)
    tweet = re.sub(r'RT\s+(@[^\s]+)\s*\:?', '', tweet)
    tweet = re.sub(r'(@[^\s]+)', '', tweet)
    tweet = re.sub(r'(#([^\s]+))', '', tweet)
    return tweet



def remove_special_unicode(text):
    if isinstance(text, str):
        text = text.decode("utf-8", "ignore")
    return unidecode(text).replace("[?]", "")

def analyseText(tweet):
    text = ''
    text = remove_emoji(tweet)
    text = objectRemoval(tweet)
    return text


def remove_emoji(tweet):
    if isinstance(tweet, str):
        tweet = tweet.decode("utf-8", "ignore")
    try:
        highpoints = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        highpoints = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')

    tweet = highpoints.sub(u'', tweet)
    return tweet



def correct_punctuation(text, first_capital=True):

    first_was_capital = text[0].isupper()
    def no_space_after(t, p):
        return t.replace(p + ' ', p)

    def no_space_before(t, p):
        return t.replace(' ' + p, p)

    def capitalize_first(t):
        return process_first(t, lambda x: x.capitalize())

    def lowercase_first(t):
        return process_first(t, lambda x: x.lower())

    def process_first(t, procfunc):
        fw = t.split()[0]
        tl = list(fw)
        for ti in tl:
            if ti in string.punctuation:
                return t
        tl = list(t)
        for ti in xrange(len(tl)):
            if tl[ti] not in string.punctuation and tl[ti] != ' ':
                tl[ti] = procfunc(tl[ti])
                break
        return "".join(tl)

    capital_words = ['i']
    tokens = tokenize(text)
    result = "".join([" " + i if (i not in string.punctuation
                                  and not i.startswith("'")) else i
                      for i in tokens])
    for c in ['!', '?', '.', ',', ':', ')', ']', '}', '>']:
        result = no_space_before(result, c)

    for c in ['(', '[', '{', '<']:
        result = no_space_after(result, c)

    result = result.replace('"', ' " ')
    for s in capital_words:
        rgx = re.compile(r'\b(%s)\b' % re.escape(s), re.IGNORECASE)
        result = re.sub(rgx, lambda pat: pat.group(1).capitalize(), result)
    result = " ".join([capitalize_first(s.strip()) for s in sent_tokenize(result)])
    result = re.sub('\s+', ' ', result).strip()
    if first_capital or first_was_capital:
        result = capitalize_first(result)
    elif not first_was_capital:
        result = lowercase_first(result)
    result = result.strip()
    return result

def match_similar(tweets, against, min_ratio=0.95):
    for i in xrange(len(tweets)):
        t = tweets[i]
        sim = {x['tweet']: x['ratio'] for x in t.get('similars', [])}

        for j in xrange(len(against)):
            t2 = against[j]
            if t2['_id'] == t['_id']:
                continue

            ratio = Levenshtein.ratio(strclean(t['text']), strclean(t2['text']))
            if ratio > min_ratio:
                sim[t2['_id']] = ratio
        t['similars'] = list()
        for tkey, tratio in sim.iteritems():
            t['similars'].append({"tweet": tkey, "ratio": tratio})

    return tweets


    # Radu's method for searching diagnostic tweets


def findIfDiagnostic(self, tweet):
    personalPronouns = ["i", "we", "me", "us", "our", "ours"]
    # check if certain keywords are in the piece of text
    avoidedVerbs = ["think", "believe", "thinks"]
    verblist = ["got", "diagnosed", "suffering", "suffer", "have", "ill"]
    temporalAdverbs = ["today", "now", "recently", "day", "ago", "since", "week", "days", "week", "weeks"]
    invalid = False
    for verb in verblist:
        if verb in tweet["text"].lower().split() and tweet["suspectedDisease"] in tweet["text"].lower().split():
            for avoidedVerb in avoidedVerbs:
                if avoidedVerb in tweet["text"].lower().split():
                    invalid = True
            if not invalid:
                for adverb in temporalAdverbs:
                    if adverb in tweet["text"].lower().split():
                        for pronoun in personalPronouns:
                            if pronoun in tweet["text"].lower().split():
                                splitWords = tweet["text"].lower().split()
                                differenceOfIndex = splitWords.index(tweet["suspectedDisease"]) - splitWords.index(
                                    verb)
                                differenceOfIndexPronoun = splitWords.index(verb) - splitWords.index(pronoun)
                                if differenceOfIndex <= 4 and differenceOfIndex >= 0 and differenceOfIndexPronoun > 0:
                                    return True


def findIfDiagnosticFetch(tweet, disease):
    # check if certain keywords are in the piece of text
    verblist = ["have", "got", "diagnosed with", "suffering from"]
    for verb in verblist:
        if verb + " " + disease in tweet.lower():
            # self._diagnosedTweets.append(tweet)
            return True


def findIfContainsMed(tweet, disease):
    typicalMedsFile = "/home/mladen/FinalYearProject/word_lists/typicalmeds.txt"
    atypicalMedsFile = "/home/mladen/FinalYearProject/word_lists/atypicalmeds.txt"
    typicalMeds = getSearchTermsFromFile(typicalMedsFile)
    atypicalMeds = getSearchTermsFromFile(atypicalMedsFile)

    for item in atypicalMeds:
        if item.lower() in tweet.lower():
            # self._tweetsWithAtypicalMeds.append(disease + " : " + tweet)
            return True

    for item in typicalMeds:
        if item.lower() in tweet.lower() and tweet:
            # self._tweetsWithTypicalMeds.append(disease + " : " + tweet)
            return True


def getSearchTermsFromFile(fileName):
    # os.path.join('/home/mladen/FinalYearProject/word_lists',       )
    try:
        with open(fileName, 'r') as disorderFile:
            disorderList = disorderFile.readlines()
            return disorderList
    except Exception as e:
        print "Failed to read disorders from file because:", e
        raise SystemExit


# def dependencyTree(self):
#     dependencies = self.parser.parseToStanfordDependencies("Mladen is a good guy.")
#     return dependencies

def dependencyTree(self, tweet):
    parser = stanford.StanfordDependencyParser(model_path="englishPCFG.ser.gz")
    print [parse.tree() for parse in parser.raw_parse(tweet)]

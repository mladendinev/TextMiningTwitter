__author__ = 'mladen'

import Levenshtein
from nltk.tokenize import RegexpTokenizer
import langid
from nltk.parse import stanford
from nltk import wordpunct_tokenize
from nltk.corpus import stopwords


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


# def dependencyTree(self):
#     dependencies = self.parser.parseToStanfordDependencies("Mladen is a good guy.")
#     return dependencies

def dependencyTree(self, tweet):
    parser = stanford.StanfordDependencyParser(model_path="englishPCFG.ser.gz")
    print [parse.tree() for parse in parser.raw_parse(tweet)]

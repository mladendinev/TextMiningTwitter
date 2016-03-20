__author__ = 'mladen'
from textProcessing import textPreprocessing as prs
from textProcessing import textExtractor
from tfidf import tfidf

typicalMedsFile = "/home/mladen/TextMiningTwitter/word_lists/typicalmeds.txt"
atypicalMedsFile = "/home/mladen/TextMiningTwitter/word_lists/atypicalmeds.txt"
typicalMeds = textExtractor.getTerms(typicalMedsFile)
atypicalMeds = textExtractor.getTerms(atypicalMedsFile)

def compose(*functions):
    def inner(arg):
        for f in reversed(functions):
            arg = f(arg)
        return arg
    return inner

#Pre-filter the tweets before parsing them for annotation
def filterPotentialDiagnostic(tweet):
    textPreprocessing = compose(prs.replaceAbbreviation, prs.stemming, prs.tokenizeText)
    possessivePronouns = ["i", "my", "mine", "we", "me", "u", "our"]
    potenatialVerbs = ["got", "diagnos", "suffer", "suffer", "have", "ill"]
    importantWords = tfidf().testScit()
    if len(set(textPreprocessing(tweet).split()) & set(potenatialVerbs)) > 0:
        return True
    elif len(set(textPreprocessing(tweet).split()) & set(possessivePronouns)) > 0:
        return True
    elif findIfContainsMed(tweet)[0] or findIfContainsMed(tweet)[1]:
        return True
    elif len(set(textPreprocessing(tweet).split()) & set(importantWords)) > 0:
        return True
    else:
        return False

        # if ((findIfContainsMed(tweet)[0] or findIfContainsMed(tweet)[1]) or potenatialVerbs or possessivePronouns:
        #     pass
def findIfDiagnosticFetch(tweet):
    # check if certain keywords are in the piece of text
    verblist = ["have", "got", "diagnosed with", "suffering from"]
    for verb in verblist:
        if verb + " " in tweet.lower():
            # self._diagnosedTweets.append(tweet)
            return True

def findIfContainsMed(tweet):
    containsTyp = None
    containsAtyp = None
    for item in atypicalMeds:
        if item.lower() in tweet.lower():
            check1 = True
    for item in typicalMeds:
        if item.lower() in tweet.lower():
            check2 = True
    return containsTyp, containsAtyp


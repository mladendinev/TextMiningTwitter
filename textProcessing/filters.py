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


# Radu's method for searching diagnostic tweets
def findIfDiagnostic(tweet):
    suspectedDisease = ""
    listOfDiseases = ["schizophrenia", "schizophreniform", "schizo affective", "shiz", "psychosis",
                      "delusional disorder",
                      "shared psychotic", "foile a deux", "induced psychosis", "psychotic disorder"]
    for disease in listOfDiseases:
        if disease in tweet.lower():
            suspectedDisease = disease
            print suspectedDisease

    personalPronouns = ["i", "we", "me", "us", "our", "ours"]
    # check if certain keywords are in the piece of text
    avoidedVerbs = ["think", "believe", "thinks"]
    verblist = ["got", "diagnosed", "suffering", "suffer", "have", "ill"]
    temporalAdverbs = ["today", "now", "recently", "day", "ago", "since", "week", "days", "week", "weeks"]
    invalid = False
    for verb in verblist:
        if verb in tweet.lower().split() and suspectedDisease in tweet.lower().split():
            for avoidedVerb in avoidedVerbs:
                if avoidedVerb in tweet.lower().split():
                    invalid = True
                    print "first ivalid"
            if not invalid:
                for adverb in temporalAdverbs:
                    if adverb in tweet.lower().split():
                        for pronoun in personalPronouns:
                            if pronoun in tweet.lower().split():
                                splitWords = tweet.lower().split()
                                differenceOfIndex = splitWords.index(suspectedDisease) - splitWords.index(
                                    verb)
                                differenceOfIndexPronoun = splitWords.index(verb) - splitWords.index(pronoun)
                                if differenceOfIndex <= 4 and differenceOfIndex >= 0 and differenceOfIndexPronoun > 0:
                                    return True

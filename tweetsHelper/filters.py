__author__ = 'mladen'
from tweetsHelper import tweetsOperations

# Radu's methods for searching diagnostic tweets
def findIfDiagnosticFetch(tweet):
    # check if certain keywords are in the piece of text
    verblist = ["have", "got", "diagnosed with", "suffering from"]
    for verb in verblist:
        if verb + " " in tweet.lower():
            # self._diagnosedTweets.append(tweet)
            return True

def findIfContainsMed(tweet):
    typicalMedsFile = "/home/mladen/FinalYearProject/word_lists/typicalmeds.txt"
    atypicalMedsFile = "/home/mladen/FinalYearProject/word_lists/atypicalmeds.txt"
    typicalMeds = tweetsOperations.getSearchTermsFromFile(typicalMedsFile)
    atypicalMeds = tweetsOperations.getSearchTermsFromFile(atypicalMedsFile)

    for item in atypicalMeds:
        if item.lower() in tweet.lower():
            # self._tweetsWithAtypicalMeds.append(disease + " : " + tweet)
            return True

    for item in typicalMeds:
        if item.lower() in tweet.lower() and tweet:
            # self._tweetsWithTypicalMeds.append(disease + " : " + tweet)
            return True



def findIfDiagnostic(tweet):
    suspectedDisease = ""
    listOfDiseases = ["schizophrenia","schizophreniform", "schizo affective","shiz","psychosis","delusional disorder",
                      "shared psychotic","foile a deux", "induced psychosis", "psychotic disorder"]
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

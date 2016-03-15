__author__ = 'mladen'
from database.dbOperations import dbOperations
import textPreprocessing as func

rohanSleepTweetsPos = dbOperations("remote").returnInfoExtraction("sleepTweetsTestLocal", "user.rmorris.label",
                                                                  {"user.rmorris.label": "positive"})

natalieSleepTweetsPos = dbOperations("remote").returnInfoExtraction("sleepTweetsTestLocal", "user.nberry.label",
                                                                    {"user.nberry.label": "positive"})

rohanSleepTweetsNeg = dbOperations("remote").returnInfoExtraction("sleepTweetsTestLocal", "user.rmorris.label",
                                                                  {"user.rmorris.label": "negative"})

natalieSleepTweetsNeg = dbOperations("remote").returnInfoExtraction("sleepTweetsTestLocal", "user.nberry.label",
                                                                    {"user.nberry.label": "negative"})

natalieDiagTweetsNeg = dbOperations("remote").returnInfoExtraction("AnnotatedDiagnosticData", "user.nberry.label",
                                                                   {"user.nberry.label": "negative"})

rohanDiagTweetsNeg = dbOperations("remote").returnInfoExtraction("AnnotatedDiagnosticData", "user.rmorris.label",
                                                                 {"user.rmorris.label": "negative"})

natalieDiagTweetsPos = dbOperations("remote").returnInfoExtraction("AnnotatedDiagnosticData", "user.nberry.label",
                                                                   {"user.nberry.label": "positve"})

rohanDiagTweetsPos = dbOperations("remote").returnInfoExtraction("AnnotatedDiagnosticData", "user.rmorris.label",
                                                                 {"user.rmorris.label": "positve"})

timelineTweets = dbOperations("remote").findAndReturn("timelineDiagnosedUsers2", None)


def trainingData():
    return rohanSleepTweetsPos + natalieSleepTweetsPos, rohanSleepTweetsNeg + natalieSleepTweetsNeg \
           + natalieDiagTweetsNeg + rohanDiagTweetsNeg


def returnDiagnosticPositive():
    seen = []
    text = []
    for doc in natalieDiagTweetsPos + rohanDiagTweetsPos:
        if doc['tweet_id'] not in seen:
            seen.append(doc['tweet_id'])
            print doc['tweet_id']
            text.append(func.analyseText(doc['text']))
    return text, seen


def returnDiagnosticNeg():
    seen = []
    text = []
    for doc in natalieDiagTweetsPos + rohanDiagTweetsPos:
        if doc['tweet_id'] not in seen:
            seen.append(doc['tweet_id'])
            text.append(func.analyseText(doc['text']))
    return text


def returnSleepPos():
    seen = []
    text = []
    for doc in natalieSleepTweetsPos + rohanSleepTweetsNeg + rohanSleepTweetsPos:
        if doc['tweet_id'] not in seen:
            seen.append(doc['tweet_id'])
            text.append(func.analyseText(doc['text']))
    return text


def returnSleepNeg():
    seen = []
    text = []
    for doc in natalieSleepTweetsNeg + rohanSleepTweetsNeg:
        if doc['tweet_id'] not in seen:
            seen.append(doc['tweet_id'])
            text.append(func.analyseText(doc['text']))
    return text

    # for tweet in positiveTweets:
    #     print tweet
    #     print '\n'

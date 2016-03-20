__author__ = 'mladen'
# Copyright (c) 2016 year Mladen Dinev.
# May be used free of charge.
# Selling without prior written consent prohibited.
# Obtain permission before redistributing.
# In all cases this notice must remain intact.
from textProcessing import dataAnalysis as data
from pylab import *
from database.dbOperations import dbOperations as db
from seaborn.distributions import distplot
from matplotlib import pyplot as plt
import numpy as np
from textProcessing.sklearnPack.metricsClassifier import timestampFigure

def frawFigure():
    figure(1, figsize=(6, 6))
    ax = axes([0.1, 0.1, 0.8, 0.8])

    labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
    fracs = [15, 30, 45, 10]
    explode = (0, 0.05, 0, 0)

    pie(fracs, explode=explode, labels=labels,
        autopct='%1.1f%%', shadow=True, startangle=90)

    title('Raining Hogs and Dogs', bbox={'facecolor': '0.8', 'pad': 5})
    show()


def lexical_diversity():
    set1 = data.returnDiagnosticNeg() + data.returnDiagnosticPositive()[0]
    set2 = data.returnSleepNeg() + data.returnSleepPos()
    diagnosticDataset = ' '.join(set1)
    print
    sleepDataset = ''.join(set2)
    return (float(len(set(diagnosticDataset))) / len(diagnosticDataset)), \
           float(len(set(sleepDataset))) / len(sleepDataset)


def proportionTweets():
    print 'dsada'
    the_grid = GridSpec(2, 2)
    labels = 'Positive', 'Negative'
    totalSleep = len(
        data.natalieSleepTweetsNeg + data.natalieSleepTweetsPos + data.rohanSleepTweetsNeg + data.rohanSleepTweetsPos)
    totalDiagn = len(
        data.natalieDiagTweetsNeg + data.natalieSleepTweetsPos + data.rohanSleepTweetsNeg + data.rohanSleepTweetsPos)
    fractionPositiveSleep = float(len(data.natalieDiagTweetsPos + data.rohanDiagTweetsPos)) / totalSleep * 100
    fractionPositiveDiagn = float(len(data.natalieDiagTweetsPos + data.rohanDiagTweetsPos)) / totalDiagn * 100
    fractionSleep = [fractionPositiveSleep, 100 - fractionPositiveSleep]
    fractionDiagn = [fractionPositiveDiagn, 100 - fractionPositiveDiagn]
    fig = plt.figure(figsize=(10, 7))
    explode = (0, 0.05)
    colors = ['green', 'red']
    ax = plt.subplot(the_grid[0, 0], aspect=1)
    ax.set_title("Sleep-related Tweets")
    plt.pie(fractionSleep, labels=labels, autopct='%1.1f%%', shadow=True, colors=colors, explode=explode)

    ax = plt.subplot(the_grid[0, 1], aspect=1)
    ax.set_title("Diagnostic Tweets")
    plt.pie(fractionDiagn, explode=explode, colors=colors, labels=labels, autopct='%.0f%%', shadow=True)
    plt.show()


def histogramHours():
    hours = [(doc['local_time_tweet']).hour for doc in data.timelineTweets if doc['local_time_tweet'] != None]
    hours = np.asarray(hours)
    ax = distplot(hours, hist=True, axlabel="Timeline hours distribution")
    plt.show()


def numbDiagnostic():
    numberDiagnosticTweets = db("remote").countTweetsInDatabase("diagnosticTweets") + \
                             db("remote").countTweetsInDatabase("newDiagnostic") + \
                             db("remote").countTweetsInDatabase("streamDiagnostic")
    return numberDiagnosticTweets


def trainDataSleep():
    return db("remote").countTweetsInDatabase("sleepTweetsTestLocal")


def timelineTweets():
    return db("remote").countTweetsInDatabase("timelineDiagnosedUsers2")


def semnaticVariety():
    return db("remote").semanticVariety("timelineDiagnosedUsers2")


def hisotgramSentiment():
    positiveSentiment, negativeSentiment = db("remote").returnSemanticTrends()
    myarray1 = np.asarray(positiveSentiment)
    myarray2 = np.asarray(negativeSentiment)
    # for item in p:
    #     item.set_height(item.get_height()/sum(x))
    plt.figure()
    plt.xlabel("Days after and before the diagnosis")
    x = [positiveSentiment,negativeSentiment]

    # ax = distplot(myarray1,hist=True,axlabel="Timeline hours distribution",norm_hist=True)
    ax = plt.hist([myarray1, myarray2], stacked=False, normed=True, label=["Positive", "Negative"])
    plt.savefig("/home/mladen/TextMiningTwitter/textProcessing/sklearnPack/screenshots/" + timestampFigure() + "SentimentDistribution")
    plt.legend()
    plt.show()

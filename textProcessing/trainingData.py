__author__ = 'mladen'
from database.dbOperations import dbOperations

rohanSleepTweetsPos = dbOperations("remote").returnSpecTweets("sleepTweetsTestLocal", "user.rmorris.label",
                                                              {"user.rmorris.label":"positive"})

natalieSleepTweetsPos = dbOperations("remote").returnSpecTweets("sleepTweetsTestLocal", "user.nberry.label",
                                                                {"user.nberry.label":"positive"})

rohanSleepTweetsNeg = dbOperations("remote").returnSpecTweets("sleepTweetsTestLocal", "user.rmorris.label",
                                                              {"user.rmorris.label":"negative"})

natalieSleepTweetsNeg = dbOperations("remote").returnSpecTweets("sleepTweetsTestLocal", "user.nberry.label",
                                                                {"user.nberry.label":"negative"})

natalieDiagTweetsNeg = dbOperations("remote").returnSpecTweets("diagnosticTweets", "user.nberry.label",
                                                               {"user.nberry.label":"negative"})

rohanDiagTweetsNeg = dbOperations("remote").returnSpecTweets("diagnosticTweets", "user.rmorris.label",
                                                             {"user.rmorris.label":"negative"})

def splitDataset():
    seen = []
    negativeExamples = []
    for tweet in rohanDiagTweetsNeg + natalieSleepTweetsPos :
        if tweet["tweet_id"] not in seen:
            seen.append(tweet["tweet_id"])
            tupple = (tweet['text'],tweet['label'])

    for tweet in rohanSleepTweetsNeg + natalieSleepTweetsNeg +natalieDiagTweetsNeg + rohanDiagTweetsNeg:
            if tweet["tweet_id"] not in seen:
                seen.append(tweet["tweet_id"])
                tupple = (tweet['text'],tweet['label'])


    print 'num',len(negativeExamples)
    negativeExamples = negativeExamples
    positiveExamples = chunk1SleepPos + chunk2SleepPos

    return positiveExamples[1:112], negativeExamples +chunk2DiagnNeg[1:80]


# def extractLocalTime():
#     featureVectorPos = []
#     seenTweet = []
#     for tweet in rohanSleepTweetsPos + natalieSleepTweetsPos:
#         if tweet["utc_offset"] != None:
#             localtime = func().calculate_localtime(tweet["created_at"], tweet["utc_offset"])
#             if localtime !=None:
#                 featureVectorPos.append(get_part_of_the_day(localtime))
#                 break
#         elif tweet["time_zone"] != None:
#             localtime = func().convertTimezoneToLocal(tweet["time_zone"])
#             if localtime !=None:
#                 featureVectorPos.append(get_part_of_the_day(localtime))
#                 break
#         else:
#             featureVectorPos.append(None)
#
#     featureVectorNeg = []
#     for tweet in rohanSleepTweetsNeg + natalieSleepTweetsNeg + natalieDiagTweetsNeg + rohanDiagTweetsNeg:
#         if tweet["utc_offset"] != None:
#             localtime = func().calculate_localtime(tweet["created_at"], tweet["utc_offset"])
#             if localtime !=None:
#                 featureVectorNeg.append(get_part_of_the_day(localtime))
#                 break
#         elif tweet["time_zone"] != None:
#             localtime = func().convertTimezoneToLocal(tweet["time_zone"])
#             if localtime !=None:
#               featureVectorNeg.append(get_part_of_the_day(localtime))
#         else:
#             featureVectorNeg.append(None)
#
#     return featureVectorPos,featureVectorNeg
#

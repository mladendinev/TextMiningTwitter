__author__ = 'mladen'
# Copyright (c) 2016 year Mladen Dinev.
# May be used free of charge.
# Selling without prior written consent prohibited.
# Obtain permission before redistributing.
# In all cases this notice must remain intact.

import createFeatureSet as models
import Classifiers

import metricsClassifier


class guiInteractions():
    def featureModel(self, featureOp):
        if featureOp == "word frequency":
            result = models.modelBagOfWords()
        elif featureOp == 'tf-idf':
            result = models.modelTfIDf()
        elif featureOp == 'part of speech tags frequency':
            result = models.modelFreqPosTag()
        elif featureOp == 'part of speech tags':
            result = models.modelPosTag()
        elif featureOp == 'part of the day':
            result = models.modelPartOfTheDay()
        elif featureOp == 'semantic classes':
            result = models.modelSemanticClasses()
        elif featureOp == 'sentiment':
            result = 0
        else:
            result = 0
            raise ValueError("The feature " + featureOp + " doesn't exist")
        return result

    def train_info(self, featureOption, classifierOption, run="Train/Test"):
        global classifier
        featureMod = self.featureModel(featureOption)
        if classifierOption == 'Dicision Tree':
            classifier = Classifiers.decisitonTree(featureMod[0], featureMod[1], featureMod[2])
        elif classifierOption == 'SVM':
            classifier = Classifiers.svc(featureMod[0], featureMod[1], featureMod[2])
        elif classifierOption == 'Multinomial Naive Bayes':
            classifier = Classifiers.multiNaiveBayes(featureMod[0], featureMod[1], featureMod[2])
        else:
            raise ValueError("The classifier doesn't exist")
        return classifier, featureMod[3],featureMod[4]

    def run(self, featureOption, classifierOption, operation):
        if operation == "Train/Test":
            classifier,vector,tweetIds = self.train_info(featureOption, classifierOption)
            return classifier[0],tweetIds
        elif operation == "Info":
            classifier,vector,tweetIds = self.train_info(featureOption, classifierOption)
            result = metricsClassifier.top10MostImportantFeautures("Freq-Pos-Tags", classifier[1],
                                                               vector)
        else:
            raise ValueError("Wrong option")
        return result

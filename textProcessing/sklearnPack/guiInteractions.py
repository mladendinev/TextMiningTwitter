__author__ = 'mladen'
# Copyright (c) 2016 year Mladen Dinev.
# May be used free of charge.
# Selling without prior written consent prohibited.
# Obtain permission before redistributing.
# In all cases this notice must remain intact.

import createFeatureSet as models
import Classifiers

import metricsClassifier

# Return the feature model with respect to the selected option
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
            result = models.modelSentiment()
        elif featureOp == "words and pos-tags":
            result = models.featuresCombined(models.modelBagOfWords(),models.modelPosTag())
        elif featureOp == "tf-idf and semantic classes":
            result = models.featuresCombined(models.modelTfIDf(),models.modelSemanticClasses())
        else:
            raise ValueError("The feature " + featureOp + " doesn't exist")
        return result

    #Predict the test instances using the specified classifier
    def train_info(self, featureOption, classifierOption, run="Train/Test"):
        global classifier
        featureMod = self.featureModel(featureOption)
        if classifierOption == 'Decision Tree':
            classifier = Classifiers.decisionTree(featureMod[0], featureMod[1], featureMod[2])
        elif classifierOption == 'SVM':
            classifier = Classifiers.svc(featureMod[0], featureMod[1], featureMod[2])
        elif classifierOption == 'Multinomial Naive Bayes':
            classifier = Classifiers.multiNaiveBayes(featureMod[0], featureMod[1], featureMod[2])
        elif classifierOption == 'Linear SVC':
            classifier = Classifiers.linearSVC(featureMod[0], featureMod[1], featureMod[2])
        else:
            raise ValueError("The classifier doesn't exist")
        return classifier, featureMod[3], featureMod[4]

    #Combine the above two methods in one method for simplicity
    def run(self, featureOption, classifierOption, operation):
        if operation == "Train/Test":
            classifier, vector, tweetIds = self.train_info(featureOption, classifierOption)
            return classifier[0], tweetIds
        elif operation == "Info":
            classifier, vector, tweetIds = self.train_info(featureOption, classifierOption)
            result = metricsClassifier.top10MostImportantFeautures("Freq-Pos-Tags", classifier[1],
                                                                   vector)
        else:
            raise ValueError("Wrong option")
        return result

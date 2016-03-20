__author__ = 'mladen'
#Copyright (c) 2016 year Mladen Dinev. 
#May be used free of charge. 
#Selling without prior written consent prohibited. 
#Obtain permission before redistributing. 
#In all cases this notice must remain intact.
from createFeatureSet import *
from Classifiers import *
import metricsClassifier
if __name__ == "__main__":
    trialData,trialTest, trainingLabels,vFeature_names, tweetIds = featuresCombined(modelSemanticClasses(),modelTfIDf())

    predicted = metricsClassifier.stratified_cv('title',vFeature_names,trialData.toarray(),trainingLabels,SVC, kernel='linear', C=1)
    metricsClassifier.classificationReport(trainingLabels, predicted)
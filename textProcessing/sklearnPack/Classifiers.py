__author__ = 'mladen'
#Copyright (c) 2016 year Mladen Dinev. 
#May be used free of charge. 
#Selling without prior written consent prohibited. 
#Obtain permission before redistributing. 
#In all cases this notice must remain intact.
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC

def multiNaiveBayes(trainingModel,testingModel,trainingLabels,):
    clf = MultinomialNB()
    clf_fit = clf.fit(trainingModel, trainingLabels)
    predicted = clf_fit.predict(testingModel)
    return predicted,clf

def randomForest(trainingModel,testingModel,trainingLabels,):
    clf = RandomForestClassifier()
    clf_fit = clf.fit(trainingModel, testingModel,trainingLabels)
    predicted = clf_fit.predict(testingModel)
    return predicted,clf

def svc(trainingModel,testingModel,trainingLabels):
    clf = SVC(kernel='linear',C=1)
    clf_fit = clf.fit(trainingModel, trainingLabels)
    predicted = clf_fit.predict(testingModel)
    return predicted,clf

def decisitonTree(trainingModel,testingModel,trainingLabels):
    clf = DecisionTreeClassifier()
    clf_fit = clf.fit(trainingModel, trainingLabels)
    predicted = clf_fit.predict(testingModel)
    return predicted,clf
__author__ = 'mladen'
import Tkinter as tk
import ScrolledText
from Tkinter import StringVar
from Tkinter import OptionMenu
from ttk import Treeview

from textProcessing import dataAnalysis as data
from textProcessing import textPreprocessing as prc
from textProcessing.sklearnPack .guiInteractions import guiInteractions as interact
class ExtractUserTimelines(tk.Frame):
    TITLE_FONT = ("Helvetica", 15, "bold")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        #
        labelTitle = tk.Label(self, text="Timeline Tweets", font=self.TITLE_FONT)
        labelTitle.grid(row=0)
        scrolledText = ScrolledText.ScrolledText(master=self,
                                                 wrap='word',  # wrap text at full words only
                                                 bg='beige', width=100)  # background color of edit area)
        for i, doc in enumerate(data.timelineTweets[:200]):
            scrolledText.insert(tk.INSERT, prc.analyseText(doc['text']) + "\n")
            scrolledText.insert(tk.INSERT, "=" * 100 + "\n")
        scrolledText.grid(row=1, column=0, padx=10, pady=10, rowspan=8)
        TITLE_FONT_MENU = ("Helvetica", 10, "bold")


        # Menu select features
        features = ['word frequency', 'tf-idf', "part of speech tags frequency",'part of speech tags',
                    'semantic classes', "part of the day", "sentiment"]

        labelSelect = tk.Label(self, text="Select a feature", font=TITLE_FONT_MENU)
        labelSelect.grid(row=1, column=1, sticky=tk.S, padx=20)
        self.selectedOp = StringVar(self)
        self.selectedOp.set(features[0])
        self.featureOption = OptionMenu(self,self.selectedOp, *features, command=self.allowButon)
        self.featureOption.grid(row=2, column=1, sticky=tk.N)

        # Menu select a classifier
        classifiers = ['Dicision Tree', 'SVM', 'Multinomial Naive Bayes']
        labelSelect = tk.Label(self, text="Select a classifier", font=TITLE_FONT_MENU)
        labelSelect.grid(row=2, column=1, sticky=tk.S, padx=20)
        self.selectedClass = StringVar(self)
        self.selectedClass.set(classifiers[0])
        self.classifierOption = OptionMenu(self,self.selectedClass, *classifiers, command=self.allowButon)
        self.classifierOption.grid(row=3, column=1, sticky=tk.N)
        self.classifierOption.config(state=tk.DISABLED)


        #Train and test
        trainLabel = tk.Label(self, text="Train and Test Classifier", font=TITLE_FONT_MENU)
        trainLabel.grid(row=3, column=1, sticky=tk.S, padx=20)
        self.train_classifier = tk.Button(self, text="Train and Test", command=self.create_window,borderwidth=2)
        self.train_classifier.grid(row=4, column=1, sticky=tk.N)

        #Informative features
        infoLabel = tk.Label(self, text="Informative fatures", font=TITLE_FONT_MENU)
        infoLabel.grid(row=5, column=1, sticky=tk.S, padx=20)
        self.infoFeatures = tk.Button(self, text="Informative fatures", command=self.showInfo,borderwidth=2)
        self.infoFeatures.grid(row=6, column=1, sticky=tk.N)
        self.infoFeatures.config(state=tk.DISABLED)

    def allowButon(self, value):
        self.classifierOption.config(state=tk.NORMAL)

    title1 = 'Extract Timelines'

    def print_it(self):
        print self.controller.app_data["tweets"]

    def trainClassifer(self):
         print 'kurec'



    def showInfo(self):
        feature = self.selectedOp.get()
        classifier = self.selectedClass.get()
        operations = interact().run(feature,classifier,'Info')
        return operations

    def create_window(self):
        #Prediction labels
        feature = self.selectedOp.get()
        classifier = self.selectedClass.get()
        predictionLabels,tweetsText = interact().run(feature,classifier,'Train/Test')

        self.infoFeatures.config(state=tk.NORMAL)
        t = tk.Toplevel(self)
        t.wm_title("Predicted Labels")
        # t.geometry("400x400")
        label = tk.Label(t, text="Predicted Labels" )
        label.pack(side=tk.LEFT, fill="both", expand=True)
        tree = Treeview(t,height=33)
        tree['columns'] = ("prediction")
        tree.column("#0",width=800)
        tree.column("prediction",width=90)
        tree.heading("prediction",text="prediction")
        tree.heading("#0",text="Raw Tweets")
        for label,tweet in zip(predictionLabels[:200],tweetsText[:200]):
             tree.insert('', 'end', text=prc.analyseText(tweet) ,values=label)
        tree.pack()
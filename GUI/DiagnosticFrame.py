__author__ = 'mladen'
import Tkinter as tk
import numpy as np
from textProcessing import dataAnalysis as data
from Tkinter import *
class DiagnosticFrame(tk.Frame):
    title1 = 'Diagnostic Frame'
    TITLE_FONT = ("Helvetica", 18, "bold")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # text = ScrolledText.ScrolledText(self)
        self.tweets = data.returnDiagnosticPositive()[0]
        label = tk.Label(self, text="Diagnostic Tweets", font=self.TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)

        self.listTweets = Listbox(self, selectmode="multiple")
        selfloadTweets = Button(self, text="Load Diagnostic Tweets", command=lambda: self.generateListBox())

        goBackToMenu = tk.Button(self, text="Go Back to Menu",
                                 command=lambda: controller.show_frame("Main Frame"))
        goBackToMenu.pack()
        selfloadTweets.pack()

        self.selectAllTweets = Button(self, text="Select All", command=lambda:self.selectAll())
        self.selectAllTweets.config(state=DISABLED)
        self.selectAllTweets.pack()

        self.deselect = Button(self, text="Select None", command=lambda:self.deselectAll())
        self.deselect.config(state=DISABLED)
        self.deselect.pack()

        self.extractTweets = Button(self, text="Extract Timeline", command=lambda:self.goToNextFrame())
        self.extractTweets.config(state=DISABLED)
        self.extractTweets.pack()
        scrollbar = Scrollbar(self)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.listTweets.config(width=75)
        self.listTweets.config(height=30)
        self.listTweets.pack(side="bottom")
        self.listTweets.config(yscrollcommand=scrollbar.set)
        #listTweets.pack(side="top", fill="both", expand=True)
        scrollbar.config(command=self.listTweets.yview)
        self.controller.data_storage["tweets"] = 'ok'

    def generateListBox(self):
        self.extractTweets.config(state=NORMAL)
        self.selectAllTweets.config(state=NORMAL)
        self.deselect.config(state=NORMAL)
        self.listTweets.config(width=0)
        for i, tweet in enumerate(self.tweets):
            self.listTweets.delete(i)
            self.listTweets.insert(i, tweet)
        self.listTweets.select_set(0)


    def extractTimeline(self):
        ids = np.asarray(data.returnDiagnosticPositive()[1])
        selectedTweetIds = ids[list(self.listTweets.curselection())]
        #print selectedTweetIds
        # text = [self.listTweets.get(idx) for idx in self.listTweets.curselection()]
        # self.controller.data_storage["timeline_users"].append(selectedTweetIds)
        self.controller.data_storage["tweets"] = selectedTweetIds

        # print values
    def selectAll(self):
        self.listTweets.select_set(0, END)

    def deselectAll(self):
        [self.listTweets.select_clear(i) for i in self.listTweets.curselection()]

    def goToNextFrame(self):
        self.extractTimeline()
        self.controller.show_frame("Extract Timelines")

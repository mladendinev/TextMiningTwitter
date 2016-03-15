__author__ = 'mladen'
import Tkinter as tk
import numpy as np
from textProcessing import dataAnalysis as data
from Tkinter import *
class DiagnosticFrame(tk.Frame):
    title1 = 'Diagnostic Frame'
    TITLE_FONT = ("Helvetica", 18, "bold")
    def extractTimeline(self):
            ids = np.asarray(data.returnDiagnosticPositive()[1])
            selectedTweetIds = ids[list(self.list.curselection())]
            print "selected Tweet Ids", selectedTweetIds
            print selectedTweetIds
            values = [self.list.get(idx) for idx in self.list.curselection()]
            return selectedTweetIds
            # print values

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # text = ScrolledText.ScrolledText(self)
        # sys.stdout = StdoutRedirector(text_box)
        label = tk.Label(self, text="Diagnostic Tweets", font=self.TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)

        listTweets = Listbox(self, selectmode="multiple")
        loadTweets = Button(self, text="Load Diagnostic Tweets", command=lambda: self.generateListBox(controller, listTweets))

        goBackToMenu = tk.Button(self, text="Go Back to Menu",
                                 command=lambda: controller.show_frame("Main Frame"))
        goBackToMenu.pack()
        loadTweets.pack()


        self.extractTweets = Button(self, text="Extract Timeline", command=lambda: controller.show_frame("Extract Timelines"))
        self.extractTweets.config(state=DISABLED)
        self.extractTweets.pack()
        scrollbar = Scrollbar(self)
        scrollbar.pack(side=RIGHT, fill=Y)

        listTweets.config(width=75)
        listTweets.config(height=30)
        listTweets.pack(side="bottom")
        listTweets.config(yscrollcommand=scrollbar.set)
        #listTweets.pack(side="top", fill="both", expand=True)
        scrollbar.config(command=listTweets.yview)

    def generateListBox(self, controller, list):
        self.extractTweets.config(state=NORMAL)
        tweets = data.returnDiagnosticPositive()[0]
        list.config(width=0)
        for i, tweet in enumerate(tweets):
            list.insert(i, tweet)
        self.controller.data_storage["tweets"] = 'ok'



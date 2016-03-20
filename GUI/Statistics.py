__author__ = 'mladen'
import Tkinter as tk
from tkFont import Font
import visualiseStats as stas
from ttk import Treeview


class Statistics(tk.Frame):
    TITLE_FONT = ("Helvetica", 18, "bold")
    title1 = 'Statistics'

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent

        label = tk.Label(self, text="Statistics from the data storage", font=self.TITLE_FONT)
        label.pack(anchor=tk.W)
        go_back_to_menu = tk.Button(self, text="Go back to menu",
                                    command=lambda: controller.show_frame("Main Frame"))
        fractionTweets = tk.Button(self, text="Proportion tweets",
                                   command=lambda: stas.proportionTweets())
        histogramHours = tk.Button(self, text="Histogram of hours distribution",
                                   command=lambda: stas.histogramHours())
        overall_statistics = tk.Button(self, text="Overall statistics",
                                       command=self.overallStatistics)

        histogramSentiment = tk.Button(self, text="Sentiment Distribution",
                                       command=lambda: stas.hisotgramSentiment())
        go_back_to_menu.pack(anchor=tk.W)
        overall_statistics.pack(anchor=tk.W)

        fractionTweets.pack(anchor=tk.W)
        histogramSentiment.pack(anchor=tk.W)
        histogramHours.pack(anchor=tk.W)


    def overallStatistics(self):
        t = tk.Toplevel(self)
        t.wm_title("Overall Statistics")
        label = tk.Label(t, text="Overall data statistics")
        label.pack(side=tk.LEFT, fill="both", expand=True)
        tree = Treeview(t)
        tree['columns'] = ("number")
        tree.column("number", width=100)
        tree.insert('', 'end', text='Diagnostic Tweets dataset', values=stas.numbDiagnostic())
        tree.insert('', 'end', text='Sleep-related Tweets dataset', values=stas.trainDataSleep())
        tree.insert('', 'end', text='Timeline Tweets', values=stas.timelineTweets())
        id = tree.insert('', 'end', text='Semantic classes')
        tree.insert(id, 'end', text='Tree')
        for key, value in stas.semnaticVariety().iteritems():
            tree.insert(id, 'end', text=key, values=value)
        tree.pack()

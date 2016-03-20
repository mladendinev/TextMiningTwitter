__author__ = 'mladen'
import Tkinter as tk
from Tkinter import *

TITLE_FONT = ("Helvetica", 18, "bold")
from MainFrame import MainFrame
from Statistics import Statistics
from DiagnosticFrame import DiagnosticFrame
from ExtractTimelinesFrame import ExtractUserTimelines

from tkFileDialog import askopenfilename


def NewFile():
    print "New File!"


def OpenFile():
    name = askopenfilename()
    print name


def About():
    print "This is a simple example of a menu"


class StdoutRedirector(object):
    def __init__(self, text_ctrl):
        self.output = text_ctrl

    def write(self, string):
        self.output.config(state="normal")
        self.output.insert("insert", string)
        self.output.config(state="disabled")


class IORedirector(object):
    def __init__(self, text_area):
        self.text_area = text_area


class TwitterAnalysisApp(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.grid(sticky=tk.N + tk.S + tk.E + tk.W)
        # container.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=tk.YES)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.data_storage = {"selected_tweets": StringVar(),
                             "test": StringVar(),
                             "timeline_users": list,
                             }
        self.frames = {}
        for F in (MainFrame, DiagnosticFrame, Statistics, ExtractUserTimelines):
            page_name = F.title1
            frame = F(container, self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        self.show_frame("Main Frame")


    def show_frame(self, page_name):
        # frame = self.frames[page_name]
        # frame.tkraise()
        # frame.winfo_toplevel().geometry("")
        for frame in self.frames.values():
            frame.grid_remove()
        frame = self.frames[page_name]
        frame.grid()
        frame.winfo_toplevel().geometry("")


app = TwitterAnalysisApp()
app.wm_title("Twitter Analysis Tool")
# app.geometry("450x150")
menubar = Menu(app)
options = Menu(menubar, tearoff=0)
options.add_command(label="Diagnostic Tweets", command=lambda: app.show_frame("Diagnostic Frame"))
options.add_command(label="Show Statistics", command=lambda: app.show_frame("Statistics"))
options.add_command(label="Main Frame", command=lambda: app.show_frame("Main Frame"))
options.add_separator()
options.add_command(label="Quit", command=lambda: app.quit())
menubar.add_cascade(label="Options", menu=options)

aboutMenu = Menu(app, tearoff=0)
aboutMenu.add_command(label="About", command='')
menubar.add_cascade(label="Help", menu=aboutMenu)
app.config(menu=menubar)
app.mainloop()

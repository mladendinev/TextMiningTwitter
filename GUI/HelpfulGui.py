import wx
from wx.lib import wordwrap
from textProcessing import dataAnalysis as data
import numpy as np


class MainFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title="Twitter Analysis Tool", pos=wx.DefaultPosition,
                          size=wx.Size(800, 600), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
        self.bSizer1 = wx.BoxSizer(wx.VERTICAL)

        filemenu = wx.Menu()
        about = filemenu.Append(wx.ID_ABOUT, "&About", " Information about this program")
        filemenu.AppendSeparator()
        quit = filemenu.Append(wx.ID_EXIT, "E&xit", " Terminate the program")
        self.Bind(wx.EVT_MENU, self.onQuit, quit)
        self.Bind(wx.EVT_MENU, self.onAboutDlg, about)
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&Menu")
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.
        self.Show(True)

        self.SetSizer(self.bSizer1)
        self.Layout()


        # self.panelOne = panel_one(self)
        # self.panelTwo = panel_two(self)
        # self.panelTwo.Hide()
        self.Centre(wx.BOTH)

    def onQuit(self, e):
        self.Close()

    def onAboutDlg(self, e):
        info = wx.AboutDialogInfo()
        info.Name = "About Twitter Analysis Tool"
        info.Version = "0.0.1 Beta"
        info.Copyright = "(C) Mladen Dinev"
        info.Description = "This is a program for tweet text mining analysis "
        info.Developers = ["Mladen Dinev"]
        info.License = "Free source"

        # Show the wx.AboutBox
        wx.AboutBox(info)

    def __del__(self):
        pass


class panel_one(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(800, 600),
                          style=wx.TAB_TRAVERSAL)
        self.frame = parent

        controlSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.widgetSizer = wx.BoxSizer(wx.VERTICAL)

        # button = wx.Button(self,-1,"Button")
        #
        # self.widgetSizer = wx.BoxSizer(wx.VERTICAL)
        # self.widgetSizer.Add(button)
        # self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.get_selected_items(tweets), self.listControl)
        loadTweetsButton = wx.Button(self, -1, u"Load Diagnostic Tweets")
        loadTweetsButton.Bind(wx.EVT_BUTTON, self.loadTweets)

        controlSizer.Add(loadTweetsButton)

        mainSizer.Add(controlSizer)
        mainSizer.Add(self.widgetSizer)

        self.frame.SetSizer(mainSizer)
        self.Show(True)

        #
        # self.timelineTweets = wx.Button(self, wx.ID_ANY, u"TimelineTweets", wx.DefaultPosition, wx.DefaultSize, 0)
        # self.timelineTweets.Bind(wx.EVT_BUTTON, self.get_selected_items())


        # sizer.Add(self.diagnosticTweets, 0, wx.ALIGN_CENTER, 5)

    def loadTweets(self, e):
        # self.widgetSizer.Add(wx.Button(self, -1, "NE MOGA DA POVARQVAM"))

        tweets = data.returnDiagnosticPositive()
        listControl = wx.ListCtrl(self.frame,-1)
        for i, j in enumerate(tweets):
            listControl.InsertStringItem(i, j)
        self.widgetSizer.Add(listControl)
        self.frame.Layout()
    # self.frame.Fit()


def changeIntroPanel(self, event):
    event.Skip()


def get_selected_items(self, tweets):
    selection = []
    self.tweetsText = np.asarray(tweets)
    current = -1
    while True:
        next = self.GetNextSelected(self.listControl, current)
        if next == -1:
            print selection
            return self.tweetsText[selection]

        selection.append(next)
        current = next


def __del__(self):
    pass


def GetNextSelected(self, list_control, current):
    return self.listControl.GetNextItem(current,
                                        wx.LIST_NEXT_ALL,
                                        wx.LIST_STATE_SELECTED)


class panel_two(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(800, 600),
                          style=wx.TAB_TRAVERSAL)
        self.bSizer5 = wx.BoxSizer(wx.VERTICAL)
        self.m_button2 = wx.Button(self, wx.ID_ANY, u"panel 2 button ", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_button3 = wx.Button(self, wx.ID_ANY, u"panel 3 button ", wx.DefaultPosition, wx.DefaultSize, 0)
        self.bSizer5.Add(self.m_button2, 0, wx.ALL, 5)
        self.bSizer5.Add(self.m_button3, 0, wx.ALL, 5)
        self.SetSizer(self.bSizer5)
        self.Layout()
        # Connect Events
        self.m_button2.Bind(wx.EVT_BUTTON, self.changeIntroPanel)
        self.m_button3.Bind(wx.EVT_BUTTON, self.addButton)

    def __del__(self):
        pass
        # Virtual event handlers, overide them in your derived class

    def changeIntroPanel(self, event):
        event.Skip()

    def addButton(self, e):
        self.m_button3 = wx.Button(self, wx.ID_ANY, u"panel 4 button ", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_button3 = wx.Button(self, wx.ID_ANY, u"panel 4 button ", wx.DefaultPosition, wx.DefaultSize, 0)

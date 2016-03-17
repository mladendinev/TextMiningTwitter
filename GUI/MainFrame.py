__author__ = 'mladen'
import Tkinter as tk
from Tkinter import StringVar
from PIL import Image, ImageTk
from Tkinter import Label

class MainFrame(tk.Frame):

    TITLE_FONT = ("Helvetica", 18, "bold")
    title1 = 'Main Frame'
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        title = tk.Label(self, text="Please select one of the options \n from the menu", font=self.TITLE_FONT)
        title.pack(fill=tk.BOTH, expand=1)

        # pathToJpeg = "/home/mladen/Desktop/twitter-sentiment.jpg"
        # image = Image.open(pathToJpeg)
        # photo = ImageTk.PhotoImage(image)
        # labelPhoto = Label(self,image=photo)
        # labelPhoto.image = photo #reference
        #
        # w = OptionMenu(self, variable, "one", "two", "three")
        # w.pack()

        #labelPhoto.pack(side = "bottom", fill =tk.BOTH, expand = True)

    # changing the title of our master widget



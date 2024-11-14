import tkinter as tk
from tkinter import *
from tkinter import ttk

#main window settings
window = tk.Tk()
window.title("OSINT APP")
window.geometry("800x600")

#labels
label1 = tk.Label(window, text="Reddit Post Locator")
label1.place(x=30,y=100)
label2 = tk.Label(window, text="Twitter/X Post Locator")
label2.place(x=30,y=150)
label3 = tk.Label(window, text="Directory to store results")
label3.place(x=30,y=200)
usage_explanation="This app is designed to look at reddit and twtter posts and download posts which match a specific search query. In order to use it just set a directory to download the results to and click scrape"
label4 = tk.Label(window, text=usage_explanation, wraplength=400)
label4.place(x=200,y=400)

#entries
reddit_entry = Entry(window, width=40)
reddit_entry = reddit_entry.place(x=210,y=100)
twitter_entry = Entry(window, width=40)
twitter_entry = twitter_entry.place(x=210,y=150)
dir_entry = Entry(window, width=35)
dir_entry = dir_entry.place(x=260,y=200)

#buttons
reddit_button = tk.Button(window, text="Scrape!", command=lambda: print("Button clicked!"))
reddit_button.place(x=650,y=95)
twitter_button = tk.Button(window, text="Scrape!", command=lambda: print("Button clicked!"))
twitter_button.place(x=650,y=145)

#start the window loop
window.mainloop()

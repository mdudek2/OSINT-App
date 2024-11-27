import praw
from praw import reddit
from praw.models import MoreComments, user
from praw.models.reddit import comment
import tkinter as tk
from tkinter import *
from tkinter import ttk
import asyncio
from twikit import Client
import os
import csv
os.environ["PYTHONIOENCODING"] = "utf-8"

# Author: Maks Dudek
# Email: mdudek2@hawk.iit.edu
# Description: This is a simple GUI app which can scrape the top reddit posts and
# comments for each of those posts and print them to a csv  file for simple
# data analysis. This app can also search for twitter posts.

# dependencies: pip, praw, twikit

# REDDIT SCRAPE FUNCTION
def reddit_scrape():

    # get data from entries in the GUI
    subreddit_name = r_sub.get()
    query = r_search.get()
    save_location = r_dir.get()

    # variables to control how many posts and comments to retrieve
    num_posts = 10
    num_comments = 10

    # API CREDENTIALS NEEDED TO USE PRAW. LEFT BLANK ON GITHUB FOR SECURITY REASONS.
    # make an account on https://www.reddit.com/prefs/apps to get credentials.
    username = r_user.get()
    password = r_pass.get()
    client_id = r_id.get()
    client_secret = r_secret.get()

    # Initialize Reddit API client
    reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent='test', username=username,password=password)

    # Open CSV file to write posts to
    with open(save_location + "_posts.csv", mode="w", newline="", encoding="utf-8") as posts_file:

        # create a writer object to access the file and print headers for data
        posts_writer = csv.writer(posts_file)
        posts_writer.writerow(["URL", "linkedURL", "Subreddit", "Title", "User", "Upvotes", "Replies", "ID", "Post Text"])

        # Loop through posts
        for submission in reddit.subreddit(subreddit_name).search(query, limit = num_posts):
            posts_writer.writerow(["https://www.reddit.com" + submission.permalink, submission.url, submission.subreddit,
            submission.title, submission.author, submission.score, submission.num_comments,
            submission.id,submission.selftext])

    # open a new csv file to scrape for comments
    with open(save_location + "_comments.csv", mode = "w", newline="", encoding = "utf-8") as comments_file:

        # create headers for new csv file
        comment_writer = csv.writer(comments_file)
        comment_writer.writerow(["URL", "Subreddit", "Title", "Commenter", "Upvotes", "Text"])

        # iterate through posts
        for submission in reddit.subreddit(subreddit_name).search(query, limit = num_posts):

            # load comments in post
            submission.comments.replace_more(limit=0)

            # iterate through comments and write to seperate csv file
            for comment in submission.comments[:num_comments]:
                comment_writer.writerow(["https://www.reddit.com" + submission.permalink,submission.subreddit,
                submission.title,comment.author,comment.score,comment.body])

# Twitter/X SCRAPE FUNCTION

def twitter_scrape():

    # twitter login credentials. Left blank on Github for security reasons.
    # You can use your own twitter account to login.
    USERNAME = t_user.get()
    EMAIL = t_email.get()
    PASSWORD = t_pass.get()

    # get the values from the entries
    twitter_search = t_query.get()
    twitter_save = t_dir.get()

    # Initialize client
    client = Client("en-US")

    # login to twitter using asyncio
    async def main():

        await client.login(
            auth_info_1=USERNAME,
            auth_info_2=EMAIL,
            password=PASSWORD
        )

        # search for top tweets
        tweet_count = 0
        tweets = await client.search_tweet(twitter_search, "top")

        # open csv file to save twitter posts
        with open(twitter_save + ".csv", mode = "a", newline ="", encoding ="utf-8") as twitter_posts_file:
            twitter_post_writer = csv.writer(twitter_posts_file)
            twitter_post_writer.writerow(["ID", "User", "Text", "Date", "Retweets", "Favorites"])

            # iterate through tweets and export them to csv file
            for tweet_count, tweet in enumerate(tweets[:25]):
                twitter_post_writer.writerow([tweet.id,tweet.user.screen_name,tweet.text,tweet.created_at,
                tweet.retweet_count,tweet.favorite_count])

    asyncio.run(main())

# GUI CODE
# main window settings
window = tk.Tk()
window.title("OSINT APP")
window.geometry("800x600")
window.resizable(False, False)
window.configure(bg = "lavender")
# labels

# Title
title_label = tk.Label(window, text="Reddit and Twitter Scraper")
title_label.place(x=200, y=25)
title_label.config(font=("Arial", 24, "bold"))
title_label.configure(bg = "whitesmoke")

# reddit
reddit_label = tk.Label(window, text="Subreddit to search in EX: politics")
reddit_label.place(x=30, y=100)
reddit_search_label = tk.Label(window, text="Search Query. EX: Trump")
reddit_search_label.place(x=30, y=150)
reddit_save_location_label = tk.Label(window, text="Directory to store results")
reddit_save_location_label.place(x=30, y=200)
reddit_label.configure(bg = "whitesmoke")
reddit_search_label.configure(bg = "whitesmoke")
reddit_save_location_label.configure(bg = 'whitesmoke')

# twitter
twitter_label = tk.Label(window, text="Twitter Search Query EX: Trump")
twitter_label.place(x=30, y=300)
twitter_save_location_label = tk.Label(window, text="Directory to store results")
twitter_save_location_label.place(x=30, y=350)
twitter_label.configure(bg = "whitesmoke")
twitter_save_location_label.configure(bg = "whitesmoke")

# entryvars

# reddit
r_sub = tk.StringVar(value="politics")
r_search = tk.StringVar(value="Trump")
r_dir = tk.StringVar(value="Enter a Save Location with filename at the end")

r_user = tk.StringVar(value="reddit username")
r_pass = tk.StringVar(value="reddit password")
r_id = tk.StringVar(value="Client ID")
r_secret = tk.StringVar(value="Client Secret")

# twitter
t_query = tk.StringVar(value="Trump")
t_dir = tk.StringVar(value="Enter a Save Location with filename at the end")

t_email = tk.StringVar(value="Twitter acc email")
t_user = tk.StringVar(value="Twitter username")
t_pass = tk.StringVar(value="Twitter password")
# entries

# reddit
reddit_entry = Entry(window, width=29, textvariable=r_sub)
reddit_entry.place(x=220, y=100)
reddit_search_entry = Entry(window, width=35, textvariable=r_search)
reddit_search_entry.place(x=185, y=150)
reddit_save_entry = Entry(window, width=60, textvariable=r_dir)
reddit_save_entry.place(x=185, y=200)
reddit_entry.configure(bg = "whitesmoke")
reddit_search_entry.configure(bg = "whitesmoke")


r_user_entry = Entry(window, width=20, textvariable=r_user)
r_pass_entry = Entry(window, width=20, textvariable=r_pass)
r_id_entry = Entry(window, width=20, textvariable=r_id)
r_secret_entry = Entry(window, width=20, textvariable=r_secret)
r_user_entry.place(x=100, y=450)
r_pass_entry.place(x=100, y=475)
r_id_entry.place(x=100,y=500)
r_secret_entry.place(x=100,y=525)
# twitter


twitter_entry = Entry(window, width=29, textvariable=t_query)
twitter_entry.place(x=220, y=300)
twitter_save_entry = Entry(window, width=60, textvariable=t_dir)
twitter_save_entry.place(x=182, y=350)
twitter_entry.configure(bg = "whitesmoke")
twitter_save_entry.configure(bg = "whitesmoke")

t_email_entry = Entry(window, width=20,textvariable=t_email)
t_user_entry = Entry(window, width=20, textvariable=t_user)
t_pass_entry = Entry(window, width=20, textvariable=t_pass)
t_email_entry.place(x=250, y=450)
t_user_entry.place(x=250, y=475)
t_pass_entry.place(x=250,y=500)

# buttons

# reddit
reddit_button = tk.Button(window, text="Scrape for Posts and Comments", bg = "whitesmoke", command=lambda: reddit_scrape())
reddit_button.place(x=30, y=250)

# twitter
twitter_button = tk.Button(window, text="Scrape for Tweats", bg = "whitesmoke", command=lambda: twitter_scrape())
twitter_button.place(x=30, y=400)

# start the window loop
window.mainloop()

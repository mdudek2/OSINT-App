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
# Description: This is a simple GUI app which can scrape the top 5 reddit posts and
# top 5 comments for each of those posts and print them to a txt file for simple.
# data analysis. This app can also search for twitter posts and their replies.

# dependencies: pip, praw, twikit


# REDDIT SCRAPE FUNCTION
def reddit_scrape():
    subreddit_name = r_sub.get()
    query = r_search.get()
    save_location = r_dir.get()

    # API CREDENTIALS FOR PRAW. LEFT BLANK ON GITHUB FOR SECURITY REASONS.
    # make an account on https://www.reddit.com/prefs/apps to get credentials.
    username = ""
    password = ""
    client_id = ""
    client_secret = ""

    reddit_instance = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        username=username,
        password=password,
        user_agent="OSINT Post Scraper"
    )

    # create a reddit instance and search for the query. limit to only 5 posts that match query.
    subreddit = reddit_instance.subreddit(subreddit_name)
    search_results = subreddit.search(query, limit=5)

    # number of posts and comments to extract
    num_of_posts = 5
    num_of_comments = 5
    # open csv file using with open and csv writer
    with open(save_location + ".csv", mode = "a", newline='', encoding = "utf-8") as posts_file:

        post_writer = csv.writer(posts_file)
        # make the header row for the data in the csv file
        post_writer.writerow(['URL','linkedURL','Subreddit', 'Title', 'User', 'Upvotes', 'Replies', 'ID'])

        # loop through posts and add data to csv file using csv writer
        for post in subreddit.search(query, limit = num_of_posts):
            post_writer.writerow(["https://www.reddit.com" + post.permalink, post.url, post.subreddit, post.title, post.author, post.score, post.num_comments, post.id])

    # open a new csv file to scrape for comments
    with open(save_location + "_comments.csv", mode = "a", newline='', encoding = "utf-8") as comments_file:

        # create headers for new csv file
        comment_writer = csv.writer(comments_file)
        comment_writer.writerow(['URL', 'Subreddit', 'Title', 'Commenter', 'Upvotes', 'Text'])

        # iterate through posts
        for post in subreddit.search(query, limit = num_of_posts):

            # load comments in post
            post.comments.replace_more(limit=0)

            # iterate through comments and write to seperate csv file
            for comment in post.comments[:num_of_comments]:
                comment_writer.writerow(["https://www.reddit.com" + post.permalink,post.subreddit,post.title,comment.author,comment.score,comment.body])

# Twitter/X SCRAPE FUNCTION

def twitter_scrape():

    # twitter login credentials. Left blank on Github for security reasons.
    # You can use your own twitter account to login.
    USERNAME = ''
    EMAIL = ''
    PASSWORD = ''

    # get the values from the entries
    twitter_search = t_query.get()
    twitter_save = t_dir.get()

    # Initialize client
    client = Client('en-US')

    # login to twitter using asyncio
    async def main():
        await client.login(
            auth_info_1=USERNAME,
            auth_info_2=EMAIL,
            password=PASSWORD
        )
        # search for top tweets
        tweet_count = 0
        tweets = await client.search_tweet(twitter_search, 'top')

        # open csv file to save twitter posts
        with open(twitter_save + ".csv", mode = "a", newline ="", encoding ="utf-8") as twitter_posts_file:
            twitter_post_writer = csv.writer(twitter_posts_file)
            twitter_post_writer.writerow(['ID', 'User', 'Text', 'Date', 'Retweets', 'Favorites'])

            # iterate through tweets and export them to csv file
            for tweet_count, tweet in enumerate(tweets[:10]):
                twitter_post_writer.writerow([tweet.id,tweet.user.screen_name,tweet.text,tweet.created_at,tweet.retweet_count,tweet.favorite_count])

    asyncio.run(main())






# GUI CODE
# main window settings
window = tk.Tk()
window.title("OSINT APP")
window.geometry("800x600")
window.resizable(False, False)

# labels

# Title
title_label = tk.Label(window, text="Reddit and Twitter Scraper")
title_label.place(x=90, y=25)
title_label.config(font=("Arial", 24, "bold"))

# reddit
reddit_label = tk.Label(window, text="Subreddit to search in EX: politics")
reddit_label.place(x=30, y=100)
reddit_search_label = tk.Label(window, text="Search Query. EX: Trump")
reddit_search_label.place(x=30, y=150)
reddit_save_location_label = tk.Label(window, text="Directory to store results")
reddit_save_location_label.place(x=30, y=200)

# twitter
twitter_label = tk.Label(window, text="Twitter Search Query EX: Trump")
twitter_label.place(x=30, y=300)
twitter_save_location_label = tk.Label(window, text="Directory to store results")
twitter_save_location_label.place(x=30, y=350)

# entryvars

# reddit
r_sub = tk.StringVar(value="politics")
r_search = tk.StringVar(value="Trump")
r_dir = tk.StringVar(value="C:\\Users\\Maks\\Desktop\\scrapes\\reddit\\politics-Trump.txt")

# twitter
t_query = tk.StringVar(value="Trump")
t_dir = tk.StringVar(value="C:\\Users\Maks\\Desktop\\scrapes\\twitter\\Trump.txt")

# entries

# reddit
reddit_entry = Entry(window, width=29, textvariable=r_sub)
reddit_entry.place(x=220, y=100)
reddit_search_entry = Entry(window, width=35, textvariable=r_search)
reddit_search_entry.place(x=185, y=150)
reddit_save_entry = Entry(window, width=60, textvariable=r_dir)
reddit_save_entry.place(x=185, y=200)

# twitter
twitter_entry = Entry(window, width=29, textvariable=t_query)
twitter_entry.place(x=220, y=300)
twitter_save_entry = Entry(window, width=60, textvariable=t_dir)
twitter_save_entry.place(x=182, y=350)

# buttons

# reddit
reddit_button = tk.Button(window, text="Scrape for Posts and Comments", command=lambda: reddit_scrape())
reddit_button.place(x=30, y=250)

# twitter
twitter_button = tk.Button(window, text="Scrape for Tweats and replies", command=lambda: twitter_scrape())
twitter_button.place(x=30, y=400)

# start the window loop
window.mainloop()


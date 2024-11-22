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
    username = "Various-Psychology94"
    password = "M4Xyii278!"
    client_id = "4F8LeDgM4W6i007Ea8Neiw"
    client_secret = "jB2_CF5s3rrmhVH7KaUaDwC0m2DEYw"

    reddit_instance = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        username=username,
        password=password,
        user_agent="OSINT Post Scraper"
    )

    # create a reddit instance and search for the query
    subreddit = reddit_instance.subreddit(subreddit_name)
    search_results = subreddit.search(query, limit=5)

    # iterate through search results
    for submission in search_results:

        current_post = "https://reddit.com" + submission.permalink

        # Print post title, link and upvotes
        print("\n" + submission.title)
        print("Link:" + current_post)
        print("Upvotes: " + str(submission.score))

        # Write post title, link, and upvotes to file
        data_file = open(save_location, "a")
        data_file.write("\n" + submission.title)
        data_file.write("Link:" + current_post)
        data_file.write("Upvotes: " + str(submission.score))


        # Create a Submission instance to look through comments
        submission = reddit.Submission(reddit_instance, url=current_post)
        submission.comments.replace_more(limit=0)

        # Print top 5 comments per post and write to file
        count = 0
        for count, comment in enumerate(submission.comments[:5]):
            print(f"\nTop {count + 1} comment: {comment.body}")
            data_file.write(f"\nTop {count + 1} comment: {comment.body}")

        data_file.close()


# Twitter/X SCRAPE FUNCTION

def twitter_scrape():

    # twitter login credentials. Left blank on Github for security reasons.
    # You can use your own twitter account to login.
    USERNAME = 'mdudek25478'
    EMAIL = 'mdudek2@hawk.iit.edu'
    PASSWORD = 'B497Zaym!!05'

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

        tweets = await client.search_tweet(twitter_search, 'Top')

        # Iterate through tweets
        tweet_count = 0
        for tweet_count, tweet in enumerate(tweets[:5]):
            print("\n", tweet.user.name)
            print("\n", tweet.created_at_datetime)
            print("\n", tweet.favorite_count)
            print("\n", tweet.text)

            with open(twitter_save, "a", encoding="utf-8", errors="replace") as data_file2:
                data_file2.write(("\n" + str(tweet.user.name)))
                data_file2.write(("\n" + str(tweet.created_at_datetime)))
                data_file2.write(("\n" + str(tweet.favorite_count)))
                data_file2.write(("\n" + str(tweet.text)))

            # get the current tweet id in order to iterate through replies
            current_tweet = tweet.id
            target_tweet = await client.get_tweet_by_id(str(tweet.id))
            replies = target_tweet.replies
            reply_count = 0
            for reply_count, reply in enumerate(replies[:5]):
                ++reply_count
                print("\n\treply:", reply.text)

                # write replies to file
                with open(twitter_save, "a", encoding="utf-8", errors="replace") as data_file2:
                    data_file2.write("\n\treply:" + str(reply.text))

    asyncio.run(main())
    
# GUI CODE
# main window settings
window = tk.Tk()
window.title("OSINT APP")
window.geometry("600x500")
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

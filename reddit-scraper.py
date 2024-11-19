import praw
from praw import reddit
from praw.models import MoreComments, user
from praw.models.reddit import comment

#API CREDENTIALS FOR PRAW. LEFT BLANK ON GITHUB FOR SECURITY REASONS.
#make an account on https://www.reddit.com/prefs/apps to get credentials.
username = "your_username"
password = "your_password"
client_id = "your_id"
client_secret = "your_secret"

reddit_instance = praw.Reddit(
    client_id = client_id,
    client_secret = client_secret,
    username = username,
    password = password,
    user_agent = "OSINT post scraper"
)

subreddit = reddit_instance.subreddit("politics")
subreddit_name = "politics"

for submission in subreddit.hot(limit=5):

    current_post = "https://reddit.com" + submission.permalink

    #Print post title and upvotes
    print("\n" + submission.title)
    print("Link:" + current_post)
    print("Upvotes: " + str(submission.score))

    #Create a Submission instance to look through commnents
    submission = reddit.Submission(reddit_instance, url=current_post)
    submission.comments.replace_more(limit=0)

    # Print top 5 comments per post
    count = 0
    for count, comment in enumerate(submission.comments[:5]):
        print(f"Top {count + 1} comment: {comment.body}")

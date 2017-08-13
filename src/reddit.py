import praw
import os
import pkg_resources

# Return a list of reddit submission objects
def getPosts():
    posts = list()
    
    # Obtain a reddit instance
    reddit = praw.Reddit(client_id=os.environ['REDDIT_APP_ID'],
                         client_secret=os.environ['REDDIT_APP_SECRET'],
                         user_agent='heroku:automusiclink:v1 (by /u/moults31)',
                         username=os.environ['REDDIT_USERNAME'],
                         password=os.environ['REDDIT_PASSWORD'])
        
    # Load list of subreddits to run in
    listFile = pkg_resources.resource_filename(__name__, "../include/subredditlist.txt")
    with open(listFile) as f:
       subredditList = f.readlines()

    for entry in subredditList:
        subreddit = reddit.subreddit(str.strip(entry))
        
        # Add this entry to output list.
        # @TODO Filter out non-music posts
        for submission in subreddit.hot(limit=10):
            posts.append(submission)
    
    return posts

# Return a list of submission titles modified to
# include only song title and artist name
def formatPostTitles(posts):
    formattedTitles = list()
    
    for p in posts:
        t = p.title
        formattedTitles.append(t)
    
    return formattedTitles

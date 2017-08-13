import praw
import os
import pkg_resources
import re
import pprint
import xml.etree.ElementTree as ET

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
    listFile = pkg_resources.resource_filename(__name__, "../include/subredditlist.xml")
    subredditList = ET.parse(listFile).getroot()

    for sub in subredditList.findall('subreddit'):
        subreddit = reddit.subreddit(sub.find('name').text)
        
        # Add this entry to output list.
        for submission in subreddit.new(limit=10):
            # Filter out non-music posts
            ignorepost = False
            for flair in sub.find('ignoreflairs').findall('flair'):
                if submission.link_flair_text == flair.text:
                    ignorepost = True
            
            if ignorepost == False:
                posts.append(submission)
    
    return posts

# Return a list of submission titles processed
# to include only song title and artist name
def formatPostTitles(posts):
    formattedTitles = list()
    
    for p in posts:
        t = p.title
        formattedTitles.append(t)
        print(p.title)
        print(p.link_flair_text)
    
    return formattedTitles

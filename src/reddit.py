import praw
import os
import pkg_resources
import re
import xml.etree.ElementTree as ET
import time

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

# Return a dict of submission titles processed
# to include only song title and artist name.
# Use post IDs as keys.
def formatPostTitles(posts):
    formattedTitles = dict()
    
    for p in posts:
        t = p.title
        t = re.sub(r'^.*\.', '', t)
        t = re.sub(r'[\(\[\{].*$','',t)

        if re.search(r'-', t) != None:
            formattedTitles[p.id] = t
    
    return formattedTitles

# Reply on a given Reddit post
def addNewComment(post, comment):
    post.reply(comment)
    #Sleep for 9 minutes to appease reddit api rate limit gods
    print('made a comment. sleeping')
    time.sleep(9*60)

# Given a list of reddit posts, return all of those
# which u/AutoMusicLink has not commented in
def getPostsNotCommentedIn(posts):
    postsNotCommentedIn = list()

    for p in posts:
        shouldAdd = True
        
        p.comments.replace_more(limit=0)
        for top_level_comment in p.comments:
            if top_level_comment.author == 'AutoMusicLink':
                shouldAdd = False
                break

        if shouldAdd == True:
            postsNotCommentedIn.append(p)
    
    return postsNotCommentedIn

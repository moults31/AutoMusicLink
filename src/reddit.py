import praw
import os
import pkg_resources
import re
import xml.etree.ElementTree as ET
import time
import pprint

# Return a list of reddit submission objects
class reddit():
    def __init__(self):
        self.client = praw.Reddit(client_id=os.environ['REDDIT_APP_ID'],
                            client_secret=os.environ['REDDIT_APP_SECRET'],
                            user_agent='heroku:automusiclink:v1 (by /u/moults31)',
                            username=os.environ['REDDIT_USERNAME'],
                            password=os.environ['REDDIT_PASSWORD'])

        listFile = pkg_resources.resource_filename(__name__, "../include/subredditlist_2.xml")
        self.subredditList = ET.parse(listFile).getroot()

        self.postsinsubs = {}
        self.populate_postsinsubs()

    def populate_postsinsubs(self):
        for sub in self.subredditList.findall('subreddit'):
            subreddit = self.client.subreddit(sub.find('name').text)
            posts = []

            print("Fetching music submissions in r/" + sub.find('name').text)

            # Add this entry to output list.
            for submission in subreddit.hot(limit=200):
                # Filter out non-music posts
                ignorepost = self.shouldIgnorePost(sub, submission)

                if ignorepost == False:
                    posts.append(submission)
                    if len(posts) >= 50:
                        break
            
            formatted_posts = self.formatPostTitles(posts)
            self.postsinsubs[sub.find('name').text] = formatted_posts

            print("Found %i valid submissions" % len(formatted_posts))

        print("Done fetching music submissions")

    def shouldIgnorePost(self, sub, submission):
        ignorepost = False

        # First check if we should ignore based on flairs
        try:
            # For some subs we want to ignore posts with certain flairs
            for flair in sub.find('ignoreflairs').findall('flair'):
                if submission.link_flair_text == flair.text:
                    ignorepost = True
        except:
            # For others we only accept posts with certain flairs
            for flair in sub.find('acceptflairs').findall('flair'):
                if submission.link_flair_text == flair.text:
                    ignorepost = False
                else:
                    ignorepost = True

        if ignorepost == False:
            # Now catch special cases for specific subreddits
            if sub.find('name').text == "indieheads":
                if "FRESH" in submission.title:
                    ignorepost = False

        return ignorepost

    # Return a list of reddit submission objects
    def getPostsInSub(self, subname):
        return self.postsinsubs[subname]

    def getPostsInSubs(self):
        return self.postsinsubs

    # Return a dict of submission titles processed
    # to include only song title and artist name.
    # Use post IDs as keys.
    def formatPostTitles(self, posts):
        formattedTitles = dict()
        
        for p in posts:
            t = p.title
            
            # Eliminate sentences ending in a period
            t = re.sub(r'^.*\.', '', t)
            # Eliminate anything within brackets
            t = re.sub(r'\(.*\)','',t)
            t = re.sub(r'\[.*\]','',t)
            t = re.sub(r'\{.*\}','',t)

            if re.search(r'-', t) != None:
                formattedTitles[p.id] = t
        
        return formattedTitles

    # Reply on a given Reddit post
    def addNewComment(self, post, comment):
        post.reply(comment)
        #Sleep for 1 minute to appease reddit api rate limit gods
        time.sleep(60)

    # Given a list of reddit posts, return all of those
    # which u/AutoMusicLink has not commented in
    def getPostsNotCommentedIn(self, posts):
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

    def getSubredditNames(self):
        # Declare empty list of subreddits
        names = []

        for sub in self.subredditList.findall('subreddit'):
            names.append(sub.find('name').text)

        return names
# reddit.py dependencies
import praw
import os
import pkg_resources
import re
import xml.etree.ElementTree as ET
import time
import pprint

# services
import applemusic
import spotify

# Return a list of reddit submission objects
class reddit():
    def __init__(self, services):
        self.services = services

        self.client = praw.Reddit(client_id=os.environ['REDDIT_APP_ID'],
                            client_secret=os.environ['REDDIT_APP_SECRET'],
                            user_agent='heroku:automusiclink:v1 (by /u/moults31)',
                            username=os.environ['REDDIT_USERNAME'],
                            password=os.environ['REDDIT_PASSWORD'])

        listFile = pkg_resources.resource_filename(__name__, "../include/subredditlist_2.xml")
        self.subredditList = ET.parse(listFile).getroot()

        # dictionary with key=sub and key="title-artist" and value=(dict(key=service, value=id))
        self.tracksinsubs = dict(dict(dict()))
        self.populate_postsinsubs()

    def populate_postsinsubs(self):
        for sub in self.subredditList.findall('subreddit'):
            subreddit = self.client.subreddit(sub.find('name').text)

            sub_name = "r/" + sub.find('name').text

            # Keep track of which tracks we added for this sub for each service
            track_ids = dict()
            for service in self.services:
                track_ids[service] = list()

            quota_met = dict()

            for service in self.services:
                quota_met[service] = False

            print("Fetching 50 music submissions in r/" + sub.find('name').text)

            # Add this entry to output list.
            for submission in subreddit.hot(limit=None):
                # If all streaming services have met their quotas, exit before considering this post
                total_quotas_met = 0
                for service in self.services:
                    if quota_met[service] == True:
                        total_quotas_met = total_quotas_met + 1

                if total_quotas_met >= len(quota_met):

                    break

                # Filter out non-music posts
                ignorepost = self.shouldIgnorePost(sub, submission)

                if ignorepost == False:
                    formatted_title = self.formatPostTitle(submission)
                    # Format the post's title
                    if formatted_title != "":
                        # Set the reddit ID for it
                        try:
                            self.tracksinsubs[formatted_title]["reddit"] = submission.id
                        except:
                            self.tracksinsubs[formatted_title] = dict()
                            self.tracksinsubs[formatted_title]["reddit"] = submission.id

                        # Find the track corresponding to this post in our services
                        for service in self.services:
                            # Search for the track on the given service
                            id = service.getTrackIdFromTitle(submission.title)

                            if id == "":
                                continue

                            # Set it into the list for this service to add later
                            track_ids[service].append(id)

                            # Add it into our master dictionary
                            self.tracksinsubs[formatted_title][service.name] = id

                            if len(track_ids[service]) >= 50:
                                quota_met[service] = True
            
            # Add all the tracks we found to the playlists in each service
            for service in self.services:
                service.user_playlist_replace_tracks(service.get_playlist_ids[sub_name], track_ids[service])

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
                    
            if sub.find('name').text == "hiphopheads":
                if "FRESH" in submission.title:
                    ignorepost = False

        return ignorepost

    def fetchMorePostsInSub(self, subname):
            subreddit = self.client.subreddit(subname)
            posts = []

            print("Fetching 50 more submissions in r/" + subname)

            print("after post id:")
            print(self.lastpostidinsubs[subname])
            print("with title")
            print(self.postsinsubs[subname][self.lastpostidinsubs[subname]])

            params={"after" : self.lastpostidinsubs[subname]}

            # Add this entry to output list.
            for submission in subreddit.hot(limit=50, params=params):
                # Filter out non-music posts

                # shouldIgnorePost requires ET object from input XML
                # in order to load post flairs to be accepted or ignored
                ignorePost = False
                for element in self.subredditList.findall('subreddit'):
                    if subname == element.find('name').text:
                        ignorepost = self.shouldIgnorePost(element, submission)

                if ignorepost == False:
                    posts.append(submission)
                    if len(posts) >= 50:
                        print("Hit quota of 50.")
                        break
            
            # formatted_posts = self.formatPostTitles(posts)

            formatted_posts, trimmed_posts = self.formatPostTitles(posts)

            self.postsinsubs[subname] = formatted_posts
            self.lastpostidinsubs[subname] = trimmed_posts[-1].id

            print("Found %i valid submissions" % len(formatted_posts))

            # We already added to our member object, but return the list as well
            # in case the caller has already used the member list elements from prev calls
            return formatted_posts

    def getPostsInSub(self, subname):
        return self.postsinsubs[subname]

    def getPostsInSubs(self):
        return self.postsinsubs

    def getLastPostIdInSub(self, subname):
        return self.lastpostidinsubs[subname]

    # Format the title of a single post
    def formatPostTitle(self, p):
        t = p.title

        # Eliminate sentences ending in a period
        t = re.sub(r'^.*\.', '', t)
        # Eliminate anything within brackets
        t = re.sub(r'\(.*\)','',t)
        t = re.sub(r'\[.*\]','',t)
        t = re.sub(r'\{.*\}','',t)

        if re.search(r'-', t) != None:
            return t
        else:
            return ""

    # Return a dict of submission titles processed
    # to include only song title and artist name.
    # Use post IDs as keys.
    def formatPostTitles(self, posts):
        formattedTitles = dict()
        trimmed_posts = list()
        
        for p in posts:
            t = p.title
            
            print(p.id)

            # Eliminate sentences ending in a period
            t = re.sub(r'^.*\.', '', t)
            # Eliminate anything within brackets
            t = re.sub(r'\(.*\)','',t)
            t = re.sub(r'\[.*\]','',t)
            t = re.sub(r'\{.*\}','',t)

            if re.search(r'-', t) != None:
                formattedTitles[p.id] = t
                trimmed_posts.append(p)
        
        return formattedTitles, trimmed_posts

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
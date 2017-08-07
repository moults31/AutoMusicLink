import praw
import os
import pkg_resources


# Return a list of reddit submission objects
def getRedditPosts():
    redditposts = list()

    # Obtain a reddit instance
    reddit = praw.Reddit(client_id=os.environ['REDDIT_APP_ID'],
                        client_secret=os.environ['REDDIT_APP_SECRET'],
                        user_agent='heroku:automusiclink:v1 (by /u/moults31)',
                        username=os.environ['REDDIT_USERNAME'],
                        password=os.environ['REDDIT_PASSWORD'])
        
    # Load list of subreddits to run in
    listfile = pkg_resources.resource_filename(__name__, "../include/subredditlist.txt")
    with open(listfile) as f:
        subredditlist = f.readlines()
        
    for entry in subredditlist:
        subreddit = reddit.subreddit(str.strip(entry))

        print(subreddit.display_name)  # Output: redditdev

        # Add this entry to output list.
        # @TODO Filter out non-music posts
        for submission in subreddit.hot(limit=10):
            print(submission.title)  
            redditposts.append(submission)
            
    return redditposts
    
                                    
# Main

redditposts = getRedditPosts()
print(redditposts)
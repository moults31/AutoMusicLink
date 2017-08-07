import praw
import os
import pkg_resources
import requests
import spotipy

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

        # Add this entry to output list.
        # @TODO Filter out non-music posts
        for submission in subreddit.hot(limit=10):
            redditposts.append(submission)
            
    return redditposts
    

# Return a valid Client Access Token for 
# the Spotify Web API
def getSpotifyAuth():
    client_id = os.environ['SPOTIFY_APP_ID']
    client_secret = os.environ['SPOTIFY_APP_SECRET']

    grant_type = 'client_credentials'
    body_params = {'grant_type' : grant_type}
    url='https://accounts.spotify.com/api/token'

    r = requests.post(url, data=body_params, auth = (client_id, client_secret)) 
    t = r.json().get('access_token')
    
    return t


# Return a track for each reddit post passed in
def getSpotifyTracks(redditposts):
    t = getSpotifyAuth()
    sp = spotipy.Spotify(auth=t)
    
    for p in redditposts:
        print(p.title)
        tracks = sp.search(q=p.title, type='track')
        
        print(tracks)
        print("\n\n")
                   
                                    
# Main

redditposts = getRedditPosts()
getSpotifyTracks(redditposts)

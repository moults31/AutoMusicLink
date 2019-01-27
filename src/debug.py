# AutoMusicLink modules
import reddit
import spotify
import urlshortener
import gmusic
import applemusic
import pprint

# testing socket
import os
import requests
import webbrowser
import time
import json

# Call methods from here to test them
am = applemusic.AppleMusic()
r = reddit.reddit()

playlist_ids = am.get_playlist_ids()
subreddit_names = r.getSubredditNames()

for sub_name in subreddit_names:
    playlist_name = 'r/' + sub_name

    posts = r.getPostsInSub(sub_name)
    track_ids_to_add = am.getTrackIdsFromTitles(posts)

    print("Adding tracks to %s" % playlist_name)
    print("Found %i tracks to add" % len(track_ids_to_add))

    try:
        am.user_playlist_add_tracks(playlist_ids[playlist_name], track_ids_to_add)
    except KeyError:
        print("E: Playlist %s not found" % playlist_name)

print("done debug.py")
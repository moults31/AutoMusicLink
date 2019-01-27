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

playlist_ids = am.get_playlist_ids()

subreddit_names = reddit.getSubredditNames()

track_ids = []
track_ids.append('1334804732')

for name in subreddit_names:
    try:
        print("Adding track to %s" % name)
        am.user_playlist_add_tracks(playlist_ids['r/' + name], track_ids)
    except KeyError:
        print("E: Playlist %s not found" % name)
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



# for k in playlist_ids:
#     print(am.user_playlist_get_all_tracks(playlist_ids[k]))
#     am.user_playlist_delete_all_tracks(playlist_ids[k])
#     print(am.user_playlist_get_all_tracks(playlist_ids[k]))

subreddit_names = r.getSubredditNames()

for sub_name in subreddit_names:
    playlist_name = 'r/' + sub_name

    posts = r.getPostsInSub(sub_name)

    track_ids_to_add = am.getTrackIdsFromTitles(posts)

    try:
        print("Adding tracks to %s" % playlist_name)
        am.user_playlist_add_tracks(playlist_ids[playlist_name], track_ids_to_add)
    except KeyError:
        print("E: Playlist %s not found" % playlist_name)

print("done debug.py")
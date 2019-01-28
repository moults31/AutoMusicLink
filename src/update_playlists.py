# AutoMusicLink modules
import reddit
import spotify
import gmusic
import applemusic
import pprint
import os

with open(".env") as configfile:
    for line in configfile:
        name, var = line.partition("=")[::2]
        os.environ[name] = bytes(str(var).strip())

# Call methods from here to test them
am = applemusic.AppleMusic()
r = reddit.reddit()

playlist_ids = am.get_playlist_ids()
subreddit_names = r.getSubredditNames()

for sub_name in subreddit_names:
    playlist_name = 'r/' + sub_name

    print("Adding tracks to %s" % playlist_name)

    posts = r.getPostsInSub(sub_name)
    track_ids_to_add = am.getTrackIdsFromTitles(posts)

    print("Found %i tracks from %i searches" % (len(track_ids_to_add), len(posts)))

    try:
        am.user_playlist_add_tracks(playlist_ids[playlist_name], track_ids_to_add)
    except KeyError:
        print("E: Playlist %s not found" % playlist_name)

print("done update_playlists.py")
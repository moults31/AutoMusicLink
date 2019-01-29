# AutoMusicLink modules
import reddit
import spotify
import applemusic
import pprint
import os

with open(".env") as configfile:
    for line in configfile:
        name, var = line.partition("=")[::2]
        os.environ[name] = bytes(str(var).strip())

# Call methods from here to test them
am = applemusic.AppleMusic()
s = spotify.spotify()
r = reddit.reddit()

subreddit_names = r.getSubredditNames()

for sub_name in subreddit_names:
    playlist_name = 'r/' + sub_name
    print("Opening %s" % playlist_name)

    # 1: Get titles from reddit
    posts = r.getPostsInSub(sub_name)

    # 2: Search for titles in Apple Music and add found tracks to playlist
    print("Searching for %i titles in Apple Music..." % (len(posts)))
    track_ids_to_add = am.getTrackIdsFromTitles(posts)

    try:
        am.user_playlist_add_tracks(am.get_playlist_ids()[playlist_name], track_ids_to_add)
        print("%i tracks found and added." % (len(track_ids_to_add)))
    except KeyError:
        print("E: Playlist %s not found in Apple Music" % playlist_name)

    # 3: Search for titles in Spotify and add found tracks to playlist
    print("Searching for %i titles in Spotify..." % (len(posts)))
    track_ids_to_add = s.getTrackIdsFromTitles(posts)

    try:
        s.user_playlist_replace_tracks(s.get_playlist_ids()[playlist_name], track_ids_to_add)
        print("%i tracks found and added." % (len(track_ids_to_add)))
    except KeyError:
        print("E: Playlist %s not found in Spotify" % playlist_name)

print("done update_playlists.py")
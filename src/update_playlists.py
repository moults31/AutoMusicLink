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

# Prepare streaming services
am = applemusic.AppleMusic()
s = spotify.spotify()

services = [am, s]


# Declare reddit object.
# Object will populate itself with music posts on construction.
r = reddit.reddit(services)

subreddit_names = r.getSubredditNames()

for sub_name in subreddit_names:
    playlist_name = 'r/' + sub_name
    print("Opening %s" % playlist_name)

    # 1: Get titles from reddit
    posts = r.getPostsInSub(sub_name)

    # 2: Search for titles in Apple Music and add found tracks to playlist
    track_ids_to_add = list()

    print("Searching for %i titles in Apple Music..." % (len(posts)))
    track_ids_to_add.extend(am.getTrackIdsFromTitles(posts))
    print("%i tracks found." % (len(track_ids_to_add)))

    while len(track_ids_to_add) < 50:
        # Store these in the addendum list at this level so we don't re-search tracks we already found...
        # But they are also stored in our reddit object so the next streaming service won't need to request them again
        more_posts = r.fetchMorePostsInSub(sub_name)
        track_ids_to_add.extend(am.getTrackIdsFromTitles(more_posts))

    try:
        am.user_playlist_add_tracks(am.get_playlist_ids()[playlist_name], track_ids_to_add)
        print("%i tracks added." % (len(track_ids_to_add)))
    except KeyError:
        print("E: Playlist %s not found in Apple Music" % playlist_name)

    # 3: Search for titles in Spotify and add found tracks to playlist
    print("Searching for %i titles in Spotify..." % (len(posts)))
    track_ids_to_add = s.getTrackIdsFromTitles(posts)

    while len(track_ids_to_add) < 50:
        # Store these in the addendum list at this level so we don't re-search tracks we already found...
        # But they are also stored in our reddit object so the next streaming service won't need to request them again
        more_posts = r.fetchMorePostsInSub(sub_name)
        track_ids_to_add.append(s.getTrackIdsFromTitles(more_posts))

    try:
        s.user_playlist_replace_tracks(s.get_playlist_ids()[playlist_name], track_ids_to_add)
        print("%i tracks found and added." % (len(track_ids_to_add)))
    except KeyError:
        print("E: Playlist %s not found in Spotify" % playlist_name)

print("done update_playlists.py")
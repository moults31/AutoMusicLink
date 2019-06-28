# AutoMusicLink modules
import reddit
import applemusic
import os

with open(".env") as configfile:
    for line in configfile:
        name, var = line.partition("=")[::2]
        os.environ[name] = bytes(str(var).strip())

r = reddit.reddit()
subreddit_names = r.getSubredditNames()

am = applemusic.AppleMusic(playlist_names_to_create=subreddit_names)
services = [am]

playlist_ids = am.get_playlist_ids()
subreddit_names = r.getSubredditNames()

r.populate_postsinsubs(services)

print("done update_playlists.py")
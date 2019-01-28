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
# am = applemusic.AppleMusic()
# r = reddit.reddit()

with open(".env") as configfile:
    for line in configfile:
        name, var = line.partition("=")[::2]
        os.environ[name] = bytes(str(var).strip())

s = spotify.spotify()

print("done debug.py")
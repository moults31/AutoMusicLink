# AutoMusicLink modules
import reddit
import spotify
import urlshortener
import gmusic
import applemusic

# testing socket
import os
import requests
import webbrowser
import time
import json


os.environ['NO_PROXY'] = '127.0.0.1'
webbrowser.open_new('http://127.0.0.1:5000')

time.sleep(1)

r = requests.get('http://127.0.0.1:5000/usertoken')

while "Not initialized" in r.content:
    r = requests.get('http://127.0.0.1:5000/usertoken')

resp_json = json.loads(r.content)
print(resp_json['usertoken'])


# Call methods from here to test them
# am = applemusic.AppleMusic()

# am.get_user_playlist()

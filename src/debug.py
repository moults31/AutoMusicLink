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

os.environ['NO_PROXY'] = '127.0.0.1'

webbrowser.open_new('http://127.0.0.1:8080')

r = requests.get('http://127.0.0.1:8080/usertoken')
print(r.content)

# requests.put('http://127.0.0.1:8080/exit')

# Call methods from here to test them
# am = applemusic.AppleMusic()

# am.get_user_playlist()

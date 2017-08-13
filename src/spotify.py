import requests
import spotipy
import os
import pprint
import re
from difflib import SequenceMatcher

# Return a valid Client Access Token for
# the Spotify Web API
def getAuth():
    client_id = os.environ['SPOTIFY_APP_ID']
    client_secret = os.environ['SPOTIFY_APP_SECRET']
    
    grant_type = 'client_credentials'
    body_params = {'grant_type' : grant_type}
    url='https://accounts.spotify.com/api/token'
    
    r = requests.post(url, data=body_params, auth = (client_id, client_secret))
    t = r.json().get('access_token')
    
    return t


# Return a track url for each reddit post passed in
def getTracks(titles):
    token = getAuth()
    sp = spotipy.Spotify(auth=token)
    
    tracks = list()
    
    for t in titles:
        tracksearch = sp.search(q=t, type='track')
    
        items = tracksearch['tracks']['items']
        
        if not items:
            continue
        
        bestmatchrate = 0
        for item in items:
            #if re.search(item['name'], t) != None:
            s1 = item['name'] + ' - ' + item['artists'][0]['name']
            matchrate1 = SequenceMatcher(None, t, s1).ratio()
            s2 = item['artists'][0]['name'] + ' - ' + item['name']
            matchrate2 = SequenceMatcher(None, t, s2).ratio()
            
            matchrate = max(matchrate1,matchrate2)
            
            if matchrate > bestmatchrate:
                bestmatch = item
                bestmatchrate = matchrate
            
        tracks.append(bestmatch['external_urls']['spotify'])
        
        print(t)
        print(bestmatch['name'])

    return tracks

import requests
import spotipy
import os
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


# Return a dictionary with a track url at each key passed in
def getTracks(titles):
    token = getAuth()
    sp = spotipy.Spotify(auth=token)
    
    tracks = dict()
    
    # Iterate over both titles and keys
    for k in titles:
        t = titles[k]
        
        tracksearch = sp.search(q=t, type='track')
        items = tracksearch['tracks']['items']
        
        if not items:
            continue
        
        bestmatchrate = 0
        for item in items:
            s1 = item['name'] + ' - ' + item['artists'][0]['name']
            matchrate1 = SequenceMatcher(None, t, s1).ratio()
            s2 = item['artists'][0]['name'] + ' - ' + item['name']
            matchrate2 = SequenceMatcher(None, t, s2).ratio()
            
            matchrate = max(matchrate1,matchrate2)
            
            if matchrate > bestmatchrate:
                bestmatch = item
                bestmatchrate = matchrate
            
        tracks[k] = (bestmatch['external_urls']['spotify'])

    return tracks

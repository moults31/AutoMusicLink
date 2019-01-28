import requests
import spotipy
import spotipy.util as util
import os
import re
import pprint
from difflib import SequenceMatcher

class spotify():
    def __init__(self):
        client_id = os.environ['SPOTIFY_APP_ID']
        client_secret = os.environ['SPOTIFY_APP_SECRET']
        response_type = 'code'
        redirect_uri = 'https://github.com/moults31/AutoMusicLink'
        scope = 'playlist-modify-public user-read-email'
        username = 'moults31@gmail.com'

        # body_params = { 'client_id' : client_id,
        #                 'response_type' : response_type,
        #                 'redirect_uri' : redirect_uri,
        #                 'scopes' : scopes
        #                 }

        # url = 'https://accounts.spotify.com/authorize'
        # r = requests.get(url, data=body_params)

        token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
        print(token)

        # print(r.url)

        # self.token = self.getToken()


    # Return a valid Client Access Token for
    # the Spotify Web API
    def getToken(self):
        client_id = os.environ['SPOTIFY_APP_ID']
        client_secret = os.environ['SPOTIFY_APP_SECRET']
        
        grant_type = 'client_credentials'
        body_params = {'grant_type' : grant_type}
        url='https://accounts.spotify.com/api/token'
        
        r = requests.post(url, data=body_params, auth = (client_id, client_secret))
        t = r.json().get('access_token')
        
        return t


    # Return a dictionary with a track url at each key passed in
    def getTrackUrls(self, titles):
        token = getAuth()
        sp = spotipy.Spotify(auth=token)
        
        tracks = dict()
        
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

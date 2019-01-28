import requests
import spotipy
import spotipy.util as util
import os
import re
import pprint
from difflib import SequenceMatcher

class spotify():
    def __init__(self):
        self.client_id = os.environ['SPOTIFY_APP_ID']
        client_secret = os.environ['SPOTIFY_APP_SECRET']
        response_type = 'code'
        redirect_uri = 'https://github.com/moults31/AutoMusicLink'
        scope = 'playlist-modify-public user-read-email user-read-private'
        self.username = 'Zac Moulton'
        self.user_id = os.environ['SPOTIFY_USER_ID']

        token = util.prompt_for_user_token(self.username, scope, self.client_id, client_secret, redirect_uri)

        if token:
            self.sp = spotipy.Spotify(auth=token)
        else:
            print "Can't get token for", self.username



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

    def show_tracks(self, tracks):
        for i, item in enumerate(tracks['items']):
            track = item['track']
            print "   %d %32.32s %s" % (i, track['artists'][0]['name'],
                track['name'])

    def getUserPlaylists(self):
        playlists = self.sp.user_playlists(self.user_id)
        for playlist in playlists['items']:
            if playlist['owner']['id'] == self.user_id:
                print
                print playlist['name']
                print '  total tracks', playlist['tracks']['total']
                results = self.sp.user_playlist(self.user_id, playlist['id'],
                    fields="tracks,next")
                tracks = results['tracks']
                self.show_tracks(tracks)
                while tracks['next']:
                    tracks = self.sp.next(tracks)
                    self.show_tracks(tracks)

    def addToUserPlaylist(self):
        results = self.sp.user_playlist_add_tracks(self.user_id, '6ELsFo9tOnFkapX7U1e3BG', ['1j6xOGusnyXq3l6IryKF3G'])
        print results

import requests
import spotipy
import spotipy.util as util
import os
import re
import pprint
from difflib import SequenceMatcher

class spotify():
    def __init__(self):
        print('Starting Spotify...')
        self.name = "spotify"

        # Step 1: Get Spotify user auth token for necessary scopes
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

            # Step 2: Populate playlist id dictionary member
            #           key: playlist name
            #           value: playlist id
            self.playlist_ids = {}
            self.populate_playlist_ids()

            print ("Spotify started.")

        else:
            print("Spotify initialization failed. Could not get token.")


    def populate_playlist_ids(self):
        playlists = self.sp.user_playlists(self.user_id)
        for playlist in playlists['items']:
            try:
                if 'r/' in playlist['name']:
                    self.playlist_ids[playlist['name']] = playlist['id']
            except:
                # Skip over playlist names that python string can't handle
                continue


    # Searches for each title in the "titles" list param. 
    # Returns a list of ids containing all that were found.
    def getTrackIdsFromTitles(self, titles):
        tracks = list()
        
        for k in titles:
            t = titles[k]
            
            tracksearch = self.sp.search(q=t, type='track')
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
                
            tracks.append((bestmatch['external_urls']['spotify']))

        return tracks

    def getTrackIdFromTitle(self, t):        
        tracksearch = self.sp.search(q=t)
        items = tracksearch['tracks']['items']
        
        if not items:
            return ""
        
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
            
        return bestmatch['id']
            
        

    def get_playlist_ids(self):
        return self.playlist_ids


    def user_playlist_add_tracks(self, playlist_id, tracks):
        self.sp.user_playlist_add_tracks(self.user_id, playlist_id, tracks)


    def removeTrackFromUserPlaylist(self, playlist_id, track):
        self.sp.user_playlist_remove_all_occurrences_of_tracks(self.user_id, playlist_id, tracks)

    def user_playlist_replace_tracks(self, playlist_id, tracks):
        self.sp.user_playlist_replace_tracks(self.user_id, playlist_id, tracks)


import os
import pprint
import requests
import webbrowser
import time
import json
import datetime as dt
from difflib import SequenceMatcher

import sys
sys.path.append('src/apple-py-music')

from applepymusic import AppleMusicClient

class AppleMusic():
    def __init__(self, playlist_names_to_create=None):
        print("Starting apple music...")
        self.name = "applemusic"

        # Step 1: Start JS server to generate music user token
        os.environ['NO_PROXY'] = '127.0.0.1'
        webbrowser.open_new('http://127.0.0.1:8080')

        time.sleep(1)

        r = requests.get('http://127.0.0.1:8080/usertoken')

        while "Not initialized" in r.content:
            r = requests.get('http://127.0.0.1:8080/usertoken')

        am_usertoken = json.loads(r.content)['usertoken']

        # Step 2: Get Apple Music object
        self.client = AppleMusicClient( os.environ['APPLEMUSIC_TEAMID'],
                                        os.environ['APPLEMUSIC_KEY'],
                                        str(os.environ['APPLEMUSIC_SECRET']).replace(r'\n', '\n'),
                                        access_token=am_usertoken
                                        )

        # Step 3: Populate playlist id dictionary member
        #           key: playlist name
        #           value: playlist id
        self.playlist_ids = {}

        # If a list of new playlist names wasn't specified, populate
        if not playlist_names_to_create:
            self.populate_existing_playlist_ids()

        # Otherwise create the new playlists specified and populate their IDs in the dict
        else:
            self.populate_new_playlist_ids(playlist_names_to_create)


        print("Apple music started.")

    def getServiceName(self):
        return self.name

    def sample_code(self):
        resp = self.client.get_songs_by_isrc('US2U61726301')
        pprint.pprint(resp)


    def populate_new_playlist_ids(self, names):
        date = str(dt.datetime.now().date())

        for name in names:
            formatted_name = "r/" + name + "_" + date
            resp = self.client.user_playlist_create(formatted_name)

            # 0th index in resp['data'] is '[attributes]'
            self.playlist_ids["r/" + name] = resp['data'][0]['id']

    def populate_existing_playlist_ids(self):
        offset = 0
        resp = self.client.user_playlists(limit=20,offset=offset)

        while resp['data']:
            resp = self.client.user_playlists(limit=20,offset=offset)
            offset = offset + 20
            
            for playlist in resp['data']:
                try:
                    if "r/" in playlist['attributes']['name']:
                        self.playlist_ids[playlist['attributes']['name']] = playlist['id']
                except:
                    # Skip over playlist names that python string can't handle
                    continue


    def get_playlist_ids(self):
        return self.playlist_ids


    # Apple is a bad guy and has removed the capability to delete tracks ever.
    # Expose this one as replace and be ready to manually remove tracks before running any calling scripts :( wow
    def user_playlist_replace_tracks(self, id, track_ids):
        try:
            resp = self.client.user_playlist_add_tracks(id, track_ids)
        except requests.exceptions.HTTPError as e:
            # Report what went wrong, wait a second, and try one more time just in case.
            print("Caught requests.exceptions.HTTPError. Retrying once.")
            time.sleep(5)
            resp = self.client.user_playlist_add_tracks(id, track_ids)


    def user_playlist_add_tracks(self, id, track_ids):
        self.client.user_playlist_add_tracks(id, track_ids)
    

    def user_playlist_delete_all_tracks(self, id):
        # Returns 403. API endpoint discontinued.
        resp = self.user_playlist_get_all_tracks(id)

        for track in resp['data']:
            self.client.user_playlist_remove_track(id, track['id'])


    def user_playlist_get_all_tracks(self, id):
        return self.client.user_playlist(id, include='tracks')

    # Searches for each title in the "titles" list param. 
    # Returns a list of ids containing all that were found.
    def getTrackIdsFromTitles(self, titles):        
        tracks = list()
        
        for k in titles:
            t = titles[k]
            
            tracksearch = self.client.search(query=t)
            
            try:
                items = tracksearch['results']['songs']['data']
            except KeyError:
                continue
            
            bestmatchrate = 0
            for item in items:
                s1 = item['attributes']['name'] + ' - ' + item['attributes']['artistName']
                matchrate1 = SequenceMatcher(None, t, s1).ratio()
                s2 = item['attributes']['artistName'] + ' - ' + item['attributes']['name']
                matchrate2 = SequenceMatcher(None, t, s2).ratio()
                
                matchrate = max(matchrate1,matchrate2)
                
                if matchrate > bestmatchrate:
                    bestmatch = item
                    bestmatchrate = matchrate
                
            tracks.append(bestmatch['id'])

        return tracks

    def getTrackIdFromTitle(self, t):
        try:
            tracksearch = self.client.search(query=t)
        except:
            print("In Apple Music, failed to find track with query:")
            print(t)
            return ""
        try:
            items = tracksearch['results']['songs']['data']
        except KeyError:
            return ""
        
        bestmatchrate = 0
        for item in items:
            s1 = item['attributes']['name'] + ' - ' + item['attributes']['artistName']
            matchrate1 = SequenceMatcher(None, t, s1).ratio()
            s2 = item['attributes']['artistName'] + ' - ' + item['attributes']['name']
            matchrate2 = SequenceMatcher(None, t, s2).ratio()
            
            matchrate = max(matchrate1,matchrate2)
            
            if matchrate > bestmatchrate:
                bestmatch = item
                bestmatchrate = matchrate
            
        return bestmatch['id']
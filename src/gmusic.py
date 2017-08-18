from gmusicapi import Mobileclient
from difflib import SequenceMatcher
import os
import pprint

# Log in to Google Play Music and return logged-in service object
def login():
    service = Mobileclient()
    service.login(os.environ['GMUSICEMAIL'], os.environ['GMUSICPASSWORD'], os.environ['GMUSICID'])

    return service

# # Return a dictionary with a track url at each key passed in
def getTrackUrls(titles):
    service = login()
    tracks = dict()
    urlbase = "https://play.google.com/music/m/"

    for k in titles:
        t = titles[k]

        tracksearch = service.search(t)
        items = tracksearch['song_hits']

        if not items:
            continue

        bestmatchrate = 0
        for item in items:
            title = item['track']['title']
            artist = item['track']['title']
            
            s1 = title + ' - ' + artist
            matchrate1 = SequenceMatcher(None, t, s1).ratio()
            s2 = artist + ' - ' + title
            matchrate2 = SequenceMatcher(None, t, s2).ratio()
            
            matchrate = max(matchrate1,matchrate2)
            
            if matchrate > bestmatchrate:
                bestmatch = item
                bestmatchrate = matchrate

        tracks[k] = urlbase + bestmatch['track']['storeId']

    return tracks

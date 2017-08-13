import requests
import spotipy
import os

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


# Return a track for each reddit post passed in
def getTracks(titles):
    token = getAuth()
    sp = spotipy.Spotify(auth=token)
    
    tracks = list()
    
    for t in titles:
        print(t)
        tracksearch = sp.search(q=t, type='track')
        print(tracksearch)

        tracks.append(tracksearch)

    return tracks

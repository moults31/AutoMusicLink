import os
from apiclient.discovery import build
from oauth2client.client import GoogleCredentials
import pprint

# Get and return an Api instance using oauth
def getServiceObject():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(os.getcwd(), 'src/cred/AutoMusicLinker-333e1c92c852.json')
    
    credentials = GoogleCredentials.get_application_default()
    service = build('urlshortener', 'v1', credentials=credentials)
    
    return service


# Create and return a shortened url
def shortenUrl(longUrl):
    data = {'longUrl':longUrl}
    service = getServiceObject()
    
    request = service.url().insert(body=data)
    resp = request.execute()

    return resp['id']


# Return total clicks across all shortened urls made by AutoMusicLink
def getTotalClicks():
    service = getServiceObject()

    request = service.url().list(projection='ANALYTICS_CLICKS')
    history = request.execute()
    
    totalClicks = 0
    
    for item in history['items']:
        totalClicks = totalClicks + int(item['analytics']['allTime']['shortUrlClicks'])
    
    while 'nextPageToken' in history:
        token = history['nextPageToken']
        data = {'projection':'ANALYTICS_CLICKS', 'start_token':token}
        request = service.url().list(**data)
        history = request.execute()

        for item in history['items']:
            totalClicks = totalClicks + int(item['analytics']['allTime']['shortUrlClicks'])

    return totalClicks


# Return a list of long urls previously shortened by AutoMusicLink
def getPrevLongUrls():
    service = getServiceObject()
    
    request = service.url().list(projection='ANALYTICS_CLICKS')
    history = request.execute()
    
    urls = list()
    
    for item in history['items']:
        urls.append(item['longUrl'])

    while 'nextPageToken' in history:
        token = history['nextPageToken']
        data = {'projection':'ANALYTICS_CLICKS', 'start_token':token}
        request = service.url().list(**data)
        history = request.execute()
        
        for item in history['items']:
            urls.append(item['longUrl'])

    return urls


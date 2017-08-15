import os
import json
import ast
import pprint
from apiclient.discovery import build
from oauth2client.client import GoogleCredentials

import pprint

# Get and return an Api instance using oauth
def getServiceObject():
    pathname = os.path.join(os.getcwd(), 'src/cred/')
    
    data = ast.literal_eval(os.environ['GOOGLE_APPLICATION_CREDENTIALS_CONTENT'])
    filename = 'keyfile.json'
    
    if not os.path.exists(pathname):
        os.mkdir(pathname)

    with open(os.path.join(pathname, filename), 'w') as outfile:
        json.dump(data, outfile)
    
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(pathname, filename)

    credentials = GoogleCredentials.get_application_default()
    service = build('urlshortener', 'v1', credentials=credentials)
    
    return service

# Return a list of all previously shortened url objects
def getShortUrlObjs():
    urlObjs = list()
    
    service = getServiceObject()
    
    request = service.url().list(projection='ANALYTICS_CLICKS')
    history = request.execute()
    
    for item in history['items']:
        urlObjs.append(item)

    while 'nextPageToken' in history:
        token = history['nextPageToken']
        data = {'projection':'ANALYTICS_CLICKS', 'start_token':token}
        request = service.url().list(**data)
        history = request.execute()
        
        for item in history['items']:
            urlObjs.append(item)

    return urlObjs

# Return and print total clicks across all shortened urls made by AutoMusicLink
def getTotalClicks():
    totalClicks = 0
    
    urlObjs = getShortUrlObjs()
    
    for item in urlObjs:
        totalClicks = totalClicks + int(item['analytics']['allTime']['shortUrlClicks'])

    print(totalClicks)
    return totalClicks


# Return and print a list of long urls previously shortened by AutoMusicLink
def getPrevLongUrls():
    urls = list()
    
    urlObjs = getShortUrlObjs()
    
    for item in urlObjs:
        urls.append(item['longUrl'])

    pprint.pprint(urls)
    return urls

# Return and print the object for the shortened url that has been clicked most
def getMostClickedUrlObj():
    urlObjs = getShortUrlObjs()
    maxClicks = 0
    
    for item in urlObjs:
        if int(item['analytics']['allTime']['shortUrlClicks']) > maxClicks:
            maxClicks = int(item['analytics']['allTime']['shortUrlClicks'])
            mostClickedUrlObj = item

    pprint.pprint(mostClickedUrlObj)
    return mostClickedUrlObj

# Create and return a shortened url. If we have already shortened the passed-in
# longUrl, return the shortUrl we made previously.
def shortenUrl(longUrl):
    # Check if longUrl is in our url shortener history,
    # and return the corresponding shortUrl if so
    urlObjs = getShortUrlObjs()
    for obj in urlObjs:
        if obj['longUrl'] == longUrl:
            return obj['id']

    # longUrl wasn't in our history. Create a new shortUrl for it
    data = {'longUrl':longUrl}
    service = getServiceObject()
    request = service.url().insert(body=data)
    resp = request.execute()
    
    return resp['id']

import os
from apiclient.discovery import build

def getServiceObject():
    apiKey = os.environ['FIREBASE_APIKEY']
    service = build('urlshortener', 'v1', developerKey=apiKey)
    return service

# Create and return a shortened url
def shortenUrl(longUrl):
    data = {'longUrl':longUrl}
    service = getServiceObject()
    
    request = service.url().insert(body=data)
    r = request.execute()

    return r['id']

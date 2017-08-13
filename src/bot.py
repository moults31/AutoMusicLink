# AutoMusicLink modules
import reddit
import spotify
import urlshortener
import pprint


# Main

redditposts = reddit.getPosts()
titles = reddit.formatPostTitles(redditposts)

newUrls = spotify.getTrackUrls(titles)
existingUrls = urlshortener.getPrevLongUrls()
trackUrls = dict()

for key in newUrls:
    if not newUrls[key] in existingUrls:
        trackUrls[key] = newUrls[key]

pprint.pprint(trackUrls)

for post in redditposts:
    break
    if post.id in trackUrls:
        title = titles[post.id]
        url = trackUrls[post.id]

        shortUrl = urlshortener.shortenUrl(url)
        print(title)
        print(url)
        print(shortUrl)

urlshortener.getTotalClicks()
longUrls = urlshortener.getPrevLongUrls()
print('https://open.spotify.com/track/2l28wWKg7xLcBG3zhzw9Ts' in longUrls)
print('https://open.spotify.com/track/2l28wWKg7xLcBG3zhzw9Tss' in longUrls)

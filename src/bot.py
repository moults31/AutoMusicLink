# AutoMusicLink modules
import reddit
import spotify
import urlshortener

# Main

text1 = '''Beep boop, I'm a bot.

Click the link I made for you below to be taken to this song on Spotify, 
so you can add it to your queue and move on with your day!
    
['''
text2 = ''']('''
text3 = ''')
    
^^made ^^by ^^/u/moults31, ^^more ^^info: ^^[README](https://github.com/moults31/AutoMusicLink)'''

redditposts = reddit.getPosts()
titles = reddit.formatPostTitles(redditposts)

newUrls = spotify.getTrackUrls(titles)
existingUrls = urlshortener.getPrevLongUrls()
trackUrls = dict()

for key in newUrls:
    if not newUrls[key] in existingUrls:
        trackUrls[key] = newUrls[key]

for post in redditposts:
    if post.id in trackUrls:
        title = titles[post.id]
        url = trackUrls[post.id]

        shortUrl = urlshortener.shortenUrl(url)

        commentBody = text1 + title + text2 + shortUrl + text3
        reddit.addNewComment(post, commentBody)

urlshortener.getTotalClicks()
longUrls = urlshortener.getPrevLongUrls()

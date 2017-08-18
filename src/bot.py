# AutoMusicLink modules
import reddit
import spotify
import urlshortener
import gmusic


#########################################################
# Main

text1 = '''
    
'''

text2 = '''Beep boop, I'm a bot.

I generate links to streaming services so you can add
songs to your queue and move on with your day!


^^made ^^by ^^/u/moults31, ^^more ^^info: ^^[README](https://github.com/moults31/AutoMusicLink)'''

redditposts = reddit.getPostsNotCommentedIn(reddit.getPosts())
titles = reddit.formatPostTitles(redditposts)

trackUrls_sp = spotify.getTrackUrls(titles)
trackUrls_gm = gmusic.getTrackUrls(titles)

postNum = 0
for post in redditposts:
    if post.id in titles:
        title = titles[post.id]
    else:
        continue
    
    if (post.id not in trackUrls_sp) and (post.id not in trackUrls_gm):
        continue
    
    if post.id in trackUrls_sp:
        url_sp = trackUrls_sp[post.id]
        shortUrl_sp = urlshortener.shortenUrl(url_sp)

        text_sp = '[Spotify](' + shortUrl_sp + ''')
            
'''
    else:
        text_sp = '''Not found on Spotify
            
'''
    
    if post.id in trackUrls_gm:
        url_gm = trackUrls_gm[post.id]
        shortUrl_gm = urlshortener.shortenUrl(url_gm)

        text_gm = '[Google Play Music](' + shortUrl_gm + ''')
    
'''

    else:
        text_gm = '''Not found on Google Play Music
            
'''
    
    postNum = postNum + 1

    commentBody = title + text1 + text_sp + text_gm + text2
    reddit.addNewComment(post, commentBody)

print('Commented on ' + str(postNum) + ' posts')

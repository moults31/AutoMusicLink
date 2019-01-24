# AutoMusicLink modules
import reddit
import spotify
import urlshortener
import gmusic

# Return the url or error message for a given streaming service and post
def getTextForStreamingService(trackUrls, key, name):
    if key in trackUrls:
        url = trackUrls[key]
        shortUrl = urlshortener.shortenUrl(url)
            
        text = '[' + name + '](' + shortUrl + ''')
                
'''
    else:
        text = '''Not found on ''' + name + '''
                
'''

    return text

# Main program which combines all modules.
# Information on functionality found at Github.com/moults31/AutoMusicLink
def main():
    text1 = 'Streaming links for '
    text2 = ''':
    
'''

    text3 = '''Beep boop, I'm a bot.

I generate links to streaming services so you can add
songs to your queue and move on with your day!


^^made ^^by ^^/u/moults31, ^^more ^^info: ^^[README](https://github.com/moults31/AutoMusicLink)'''

    redditposts = reddit.getPostsNotCommentedIn(reddit.getPosts())
    titles = reddit.formatPostTitles(redditposts)

    trackUrls_sp = spotify.getTrackUrls(titles)

    postNum = 0
    for post in redditposts:
        if post.id in titles:
            title = titles[post.id]
        else:
            continue
    
        if (post.id not in trackUrls_sp):
            continue
    
        text_sp = getTextForStreamingService(trackUrls_sp, post.id, 'Spotify')
    
        postNum = postNum + 1

        commentBody = text1 + title + text2 + text_sp + text3
        reddit.addNewComment(post, commentBody)

    print('Commented on ' + str(postNum) + ' posts')


################################
# Main

main()

# AutoMusicLink modules
import reddit
import spotify
import urlshortener

# Main

text1 = '''Spotify link: ['''
text2 = ''']('''
text3 = ''')

Beep boop, I'm a bot.

I generate links to streaming services so you can add
songs to your queue and move on with your day!


^^made ^^by ^^/u/moults31, ^^more ^^info: ^^[README](https://github.com/moults31/AutoMusicLink)'''

redditposts = reddit.getPostsNotCommentedIn(reddit.getPosts())
titles = reddit.formatPostTitles(redditposts)

trackUrls = spotify.getTrackUrls(titles)

postNum = 0
for post in redditposts:
    if post.id in trackUrls:
        title = titles[post.id]
        url = trackUrls[post.id]

        shortUrl = urlshortener.shortenUrl(url)

        postNum = postNum + 1
        print('Commenting on post ' + str(postNum) + ' of ' + str(len(trackUrls)))
        commentBody = text1 + title + text2 + shortUrl + text3
        reddit.addNewComment(post, commentBody)

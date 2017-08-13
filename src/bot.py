# AutoMusicLink modules
import reddit
import spotify


# Main

redditposts = reddit.getPosts()
titles = reddit.formatPostTitles(redditposts)

tracks = spotify.getTracks(titles)

for post in redditposts:
    if post.id in tracks:
        title = titles[post.id]
        url = tracks[post.id]

        print(title)
        print(url)

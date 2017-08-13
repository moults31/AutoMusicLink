# OSS modules


# AutoMusicLink modules
import reddit
import spotify


                   
                                    
# Main

redditposts = reddit.getPosts()
tracktitles = reddit.formatPostTitles(redditposts)
tracks = spotify.getTracks(tracktitles)

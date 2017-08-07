import praw
import os

login_info = [os.environ['REDDIT_USERNAME'], os.environ['REDDIT_PASSWORD']]
client_info = [os.environ['REDDIT_APP_ID'], os.environ['REDDIT_APP_SECRET']]
user_agent = 'heroku:automusiclink:v1 (by /u/moults31)'

reddit = praw.Reddit(client_id=os.environ['REDDIT_APP_ID'],
                     client_secret=os.environ['REDDIT_APP_SECRET'],
                     user_agent='heroku:automusiclink:v1 (by /u/moults31)',
                     username=os.environ['REDDIT_USERNAME'],
                     password=os.environ['REDDIT_PASSWORD'])

print(reddit.read_only)

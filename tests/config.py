import os

credentials = dict(
    screen_name=os.environ.get('TWITTER_SCREEN_NAME'),
    consumer_key=os.environ.get('TWITTER_CONSUMER_KEY'),
    consumer_secret=os.environ.get('TWITTER_CONSUMER_SECRET'),
    secret=os.environ.get('TWITTER_OAUTH_SECRET'),
    token=os.environ.get('TWITTER_OAUTH_TOKEN')
)

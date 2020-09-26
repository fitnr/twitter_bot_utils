import os

credentials = dict(
    screen_name=os.environ.get('TWITTER_SCREEN_NAME'),
    consumer_key=os.environ.get('TWITTER_CONSUMER_KEY'),
    consumer_secret=os.environ.get('TWITTER_CONSUMER_SECRET'),
    secret=os.environ.get('TWITTER_OAUTH_SECRET'),
    token=os.environ.get('TWITTER_OAUTH_TOKEN'),
)

example_tweet = {
    "source": """<a href=\"http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>""",
    "entities": {
        "user_mentions": [{"name": "John Doe", "screen_name": "twitter", "indices": [0, 8], "id_str": "1", "id": 1}],
        "media": [],
        "hashtags": [],
        "urls": [],
        "symbols": [],
    },
    "in_reply_to_status_id_str": "318563540590010368",
    "id_str": "318565861172600832",
    "in_reply_to_user_id": 14155645,
    "text": "@twitter example tweet example tweet example tweet",
    "id": 318565861172600832,
    "in_reply_to_status_id": 318563540590010368,
    "in_reply_to_screen_name": "twitter",
    "in_reply_to_user_id_str": "14155645",
    "retweeted": None,
    "user": {
        "name": "Neil Freeman",
        "screen_name": "fitnr",
        "protected": False,
        "id_str": "6853512",
        "profile_image_url_https": "https://pbs.twimg.com/profile_images/431817496350314496/VGgzYAE7_normal.jpeg",
        "id": 6853512,
        "verified": False,
    },
}

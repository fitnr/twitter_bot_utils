import tweepy
from conf import users, apps

def create(app, screen_name):
    auth = tweepy.OAuthHandler(**apps.get(app))
    auth.set_access_token(**users.get(screen_name))
    return tweepy.API(auth)
    
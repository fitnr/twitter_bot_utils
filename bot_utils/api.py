import tweepy
import config

def create(app, screen_name):
    auth = tweepy.OAuthHandler(**config.app(app))
    auth.set_access_token(**config.user(screen_name))
    return tweepy.API(auth)
    
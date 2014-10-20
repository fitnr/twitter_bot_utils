import tweepy
from . import config

def create(app, screen_name):
    auth = tweepy.OAuthHandler(**config.app(app))
    auth.set_access_token(**config.user(screen_name))
    return tweepy.API(auth)

def check_api(api, **args):
    if api is False:
        if args.get('screen_name') and args.get('app'):
            api = create(args.get('app'), args.get('screen_name'))
        else:
            raise Exception('cannot create API')
    return api

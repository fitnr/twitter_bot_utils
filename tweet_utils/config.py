from pkg_resources import resource_stream
import yaml

config_handle = resource_stream('tweet_utils', '../conf.yaml')
config = yaml.load(config_handle)

def user(username):
    user = config['users'].get(username, None)
    if user is None:
        raise IndexError
    return user

def app(appname):
    app = config['apps'].get(appname, None)
    if app is None:
        raise IndexError
    return app

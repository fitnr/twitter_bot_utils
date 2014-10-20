from os import path
import yaml

config = None

def load_config(user_conf=None):
    '''Load a user config file or one from a standard place'''
    global config

    if config is None:

        file_name = ''

        if user_conf and path.exists(user_conf):
            file_name = user_conf

        else:
            local_conf = path.join(path.expanduser('~'), 'bots.yaml')

            if not path.exists(local_conf):
                local_conf = path.join(path.expanduser('~'), 'bots/bots.yaml')

            if path.exists(local_conf):
                file_name = local_conf

        try:
            with open(file_name, 'r') as f:
                config_handle = f.read()

            config = yaml.load(config_handle)

        except (AttributeError, IOError), e:
            if user_conf:
                msg = 'Custom config file not found: {0}'.format(user_conf)

            else:
                msg = 'Config file not found in ~/bots.yaml or ~/bots/bots.yaml'

            raise IOError(msg)

def user(username):
    load_config()
    user = config['users'].get(username, None)
    if user is None:
        raise IndexError
    return user

def app(appname):
    load_config()
    app = config['apps'].get(appname, None)
    if app is None:
        raise IndexError
    return app

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
            config = parse(file_name)

        except (AttributeError, IOError):
            if user_conf:
                msg = 'Custom config file not found: {0}'.format(user_conf)

            else:
                msg = 'Config file not found in ~/bots.yaml or ~/bots/bots.yaml'

            raise IOError(msg)


def parse(file_path):
    with open(file_path, 'r') as f:
        return yaml.load(f.read())


def user(username):
    load_config()
    user_details = config['users'].get(username, None)
    if user_details is None:
        raise IndexError
    return user_details


def app(appname):
    load_config()
    app_details = config['apps'].get(appname, None)
    if app_details is None:
        raise IndexError
    return app_details

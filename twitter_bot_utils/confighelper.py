# Copyright 2014 Neil Freeman
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import itertools
import json
from os import path, getcwd
# "FileNotFoundError" is a Py 3 thing. If we're in Py 2, we mimic it with a lambda expression.
try:
    FileNotFoundError
except NameError:
    from errno import ENOENT
    FileNotFoundError = lambda x: IOError(ENOENT, x)

import yaml
import tweepy

PROTECTED_INFO = [
    'apps',
    'users',
    'consumer_key',
    'consumer_secret',
    'key',
    'secret',
]

CONFIG_DIRS = [
    '~',
    path.join('~', 'bots'),
]

CONFIG_BASES = [
    'bots.yaml',
    'bots.json'
]

def configure(screen_name, config_file=None, app=None, **kwargs):
    """Setup a TBU config dictionary"""
    # Use passed config file, or look for it in the paths above
    config_file = find_file(config_file, CONFIG_DIRS, CONFIG_BASES)
    file_config = parse(config_file)

    kwargs = {k: v for k, v in kwargs.items() if v is not None}

    # kwargs take precendence over config file
    file_config.update(**kwargs)

    # config and keys dicts
    return setup(file_config, screen_name, app)


def parse(file_path):
    '''Parse a YAML or JSON file'''

    with open(file_path, 'r') as f:
        _, ext = path.splitext(file_path)

        if ext == '.yaml':
            return yaml.load(f.read())

        elif ext == '.json':
            return json.load(f.read())

    raise ValueError("Unrecognized config file type %s" % ext)


def find_file(config_file=None, default_directories=None, default_bases=None):
    '''Search for a config file in a list of files'''

    if config_file:
        if path.exists(path.expanduser(config_file)):
            return config_file
        else:
            raise FileNotFoundError('Custom config file not found: {}'.format(config_file))

    dirs = default_directories or [path.join('~', 'bots'), '~']
    dirs = [getcwd()] + dirs

    bases = default_bases or ['bots.yaml', 'bots.json']

    for directory, base in itertools.product(dirs, bases):
        filepath = path.expanduser(path.join(directory, base))
        if path.exists(filepath):
            return filepath

    raise FileNotFoundError('Config file not found in: ' + str([path.join(a, b) for a, b in itertools.product(dirs, bases)]))


def setup(file_config, screen_name, app=None):
    '''Return object that holds config settings.
    If screen_name is or missing, no user key/secret will be returned,
    and API object won't have an auth token for certain Twitter queries.
    '''
    config = dict()

    # Pull user and app data from the file
    user_conf = file_config.get('users', {}).get(screen_name, {})

    app = app or user_conf.get('app')
    app_conf = file_config.get('apps', {}).get(app, {})

    # Pull non-authentication settings from the file.
    # User, app, and general settings are included, in that order of preference
    update(config, file_config)
    update(config, app_conf)
    update(config, user_conf)

    try:
        keys = {
            'consumer_key': app_conf['consumer_key'],
            'consumer_secret': app_conf['consumer_secret'],
        }
    except KeyError as e:
        raise KeyError("App settings missing {}".format(e))

    try:
        if user_conf:
            keys['key'] = user_conf['key']
            keys['secret'] = user_conf['secret']

    except KeyError as e:
        raise KeyError("User settings missing {}".format(e))

    return config, keys


def update(config, updated):
    config.update({k: v for k, v in list(updated.items()) if k not in PROTECTED_INFO})


def setup_auth(**keys):
    '''Setup tweepy authentication using passed args or config file settings'''

    auth = tweepy.OAuthHandler(consumer_key=keys['consumer_key'], consumer_secret=keys['consumer_secret'])
    auth.set_access_token(key=keys['key'], secret=keys['secret'])

    return auth

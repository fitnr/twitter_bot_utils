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

import tweepy
import itertools
import yaml
import json
from os import path, getcwd
# "FileNotFoundError" is a Py 3 thing. If we're in Py 2, we mimic it with a lambda expression.
try:
    FileNotFoundError
except NameError:
    from errno import ENOENT
    FileNotFoundError = lambda x: IOError(ENOENT, x)


PROTECTED_INFO = [
    'apps',
    'users',
    'consumer_key',
    'consumer_secret',
    'key',
    'secret',
]


def configure(screen_name, file_name, directories=None, bases=None, **kwargs):
    """Setup a TBU config dictionary"""
    # Use passed config file, or look for it in the paths above
    config_file = find_file(file_name, directories, bases)
    file_config = parse(config_file)

    # kwargs take precendence over config file
    file_config.update(**kwargs)

    # config and keys dicts
    return setup(screen_name, file_config)


def parse(file_path):
    with open(file_path, 'r') as f:
        if file_path[-4:] == 'yaml':
            return yaml.load(f.read())

        elif file_path[-4:] == 'json':
            return json.load(f.read())


def find_file(config_file=None, default_directories=None, default_bases=None):
    '''Search for a file in a list of files'''

    if config_file:
        if path.exists(config_file):
            return config_file
        else:
            raise FileNotFoundError('Custom config file not found: {}'.format(config_file))

    default_directories = default_directories or []
    default_bases = default_bases or []

    dirs = [getcwd()] + default_directories

    for directory, base in itertools.product(dirs, default_bases):
        filepath = path.expanduser(path.join(directory, base))
        if path.exists(filepath):
            return filepath

    raise FileNotFoundError('Config file not found in ~/bots.{json,yaml}, ~/bots/bots.{json,yaml}, ~/botrc or ~/bots/botrc')


def setup(screen_name, file_config):
    '''Return object that holds config settings'''
    config = dict()

    # Pull user and app data from the file
    user_conf = file_config.get('users', {}).get(screen_name, {})
    app_conf = file_config.get('apps', {}).get(user_conf['app'], {})

    # Pull non-authentication settings from the file.
    # User, app, and general settings are included, in that order of preference
    update(config, file_config)
    update(config, app_conf)
    update(config, user_conf)

    keys = {
        'consumer_key': app_conf['consumer_key'],
        'consumer_secret': app_conf['consumer_secret'],
        'key': user_conf['key'],
        'secret': user_conf['secret']
    }

    return config, keys


def update(config, updated):
    config.update({k: v for k, v in list(updated.items()) if k not in PROTECTED_INFO})


def setup_auth(keys, **kwargs):
    '''Setup tweepy authentication using passed args or config file settings'''

    consumer_key = kwargs.get('consumer_key') or keys['consumer_key']
    consumer_secret = kwargs.get('consumer_secret') or keys['consumer_secret']

    key = kwargs.get('key') or keys['key']
    secret = kwargs.get('secret') or keys['secret']

    auth = tweepy.OAuthHandler(consumer_key=consumer_key, consumer_secret=consumer_secret)
    auth.set_access_token(key=key, secret=secret)

    return auth

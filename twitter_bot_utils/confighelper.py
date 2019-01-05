# -*- coding: utf-8 -*-
# Copyright 2014-17 Neil Freeman contact@fakeisthenewreal.org
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

from itertools import product
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


CONFIG_DIRS = [
    getcwd(),
    '~',
    path.join('~', 'bots'),
]

CONFIG_BASES = [
    'bots.yml',
    'bots.yaml',
    'bots.json'
]


def configure(screen_name=None, config_file=None, app=None, **kwargs):
    """
    Set up a config dictionary using a bots.yaml config file and optional keyword args.

    Args:
        screen_name (str): screen_name of user to search for in config file
        config_file (str): Path to read for the config file
        app (str): Name of the app to look for in the config file. Defaults to the one set in users.{screen_name}.
        default_directories (str): Directories to read for the bots.yaml/json file. Defaults to CONFIG_DIRS.
        default_bases (str): File names to look for in the directories. Defaults to CONFIG_BASES.
    """
    # Use passed config file, or look for it in the default path.
    # Super-optionally, accept a different place to look for the file
    dirs = kwargs.pop('default_directories', None)
    bases = kwargs.pop('default_bases', None)
    file_config = {}
    if config_file is not False:
        config_file = find_file(config_file, dirs, bases)
        file_config = parse(config_file)

    # config and keys dicts
    # Pull non-authentication settings from the file.
    # Kwargs, user, app, and general settings are included, in that order of preference
    # Exclude apps and users sections from config
    config = {k: v for k, v in file_config.items() if k not in ('apps', 'users')}

    user_conf = file_config.get('users', {}).get(screen_name, {})
    app = app or user_conf.get('app')
    app_conf = file_config.get('apps', {}).get(app, {})

    # Pull user and app data from the file
    config.update(app_conf)
    config.update(user_conf)

    # kwargs take precendence over config file
    config.update({k: v for k, v in kwargs.items() if v is not None})

    return config


def parse(file_path):
    '''Parse a YAML or JSON file.'''

    _, ext = path.splitext(file_path)

    if ext in ('.yaml', '.yml'):
        func = yaml.safe_load

    elif ext == '.json':
        func = json.load

    else:
        raise ValueError("Unrecognized config file type %s" % ext)

    with open(file_path, 'r') as f:
        return func(f)


def find_file(config_file=None, default_directories=None, default_bases=None):
    '''Search for a config file in a list of files.'''

    if config_file:
        if path.exists(path.expanduser(config_file)):
            return config_file
        else:
            raise FileNotFoundError('Config file not found: {}'.format(config_file))

    dirs = default_directories or CONFIG_DIRS
    dirs = [getcwd()] + dirs

    bases = default_bases or CONFIG_BASES

    for directory, base in product(dirs, bases):
        filepath = path.expanduser(path.join(directory, base))
        if path.exists(filepath):
            return filepath

    raise FileNotFoundError('Config file not found in {}'.format(dirs))


def setup_auth(**keys):
    '''Set up Tweepy authentication using passed args or config file settings.'''
    auth = tweepy.OAuthHandler(consumer_key=keys['consumer_key'], consumer_secret=keys['consumer_secret'])
    auth.set_access_token(
        key=keys.get('token', keys.get('key', keys.get('oauth_token'))),
        secret=keys.get('secret', keys.get('oauth_secret'))
    )
    return auth


def dump(contents, file_path):
    _, ext = path.splitext(file_path)

    if ext in ('.yaml', '.yml'):
        func = yaml.dump
        kwargs = {'canonical': False, 'default_flow_style': False, 'indent': 4}

    elif ext == '.json':
        func = json.dump
        kwargs = {'sort_keys': True, 'indent': 4}

    else:
        raise ValueError("Unrecognized config file type %s" % ext)

    with open(file_path, 'w') as f:
        func(contents, f, **kwargs)

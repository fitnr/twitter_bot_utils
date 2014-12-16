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
from os import path, getcwd
from . import helpers
# "FileNotFoundError" is a Py 3 thing. If we're in Py 2, we mimic it with a lambda expression.
try:
    FileNotFoundError
except NameError:
    from errno import ENOENT
    FileNotFoundError = lambda x: IOError(ENOENT, x)

CONFIG_DIRS = [
    '~',
    '~/bots',
]

CONFIG_BASES = [
    'botrc',
    'bots.yaml',
    'bots.json'
]

PROTECTED_INFO = [
    'apps',
    'users',
    'consumer_key',
    'consumer_secret',
    'key',
    'secret',
]


def _find_config_file(config_file=None):
    '''Search for a file in a list of files'''

    if config_file:
        if path.exists(config_file):
            return config_file
        else:
            raise FileNotFoundError('Custom config file not found: {}'.format(config_file))

    dirs = [getcwd()] + CONFIG_DIRS

    for directory, base in itertools.product(dirs, CONFIG_BASES):
        filepath = path.expanduser(path.join(directory, base))
        if path.exists(filepath):
            return filepath

    raise FileNotFoundError('Config file not found in ~/bots.{json,yaml}, ~/bots/bots.{json,yaml}, ~/botrc or ~/bots/botrc')


def _config_setup(cls, file_config):
    '''Return object that holds config settings'''

    # Pull user and app data from the file
    user_conf = file_config.get('users', {}).get(cls.screen_name, {})
    app_conf = file_config.get('apps', {}).get(user_conf['app'], {})

    # Pull non-authentication settings from the file.
    # User, app, and general settings are included, in that order of preference
    cls.update_config(file_config)
    cls.update_config(app_conf)
    cls.update_config(user_conf)

    return {
        'consumer_key': app_conf.get('consumer_key'),
        'consumer_secret': app_conf.get('consumer_secret'),
        'key': user_conf.get('key'),
        'secret': user_conf.get('secret')
    }


def _setup_auth(conf, **kwargs):
    '''Setup tweepy authentication using passed args or config file settings'''

    consumer_key = kwargs.get('consumer_key') or conf['consumer_key']
    consumer_secret = kwargs.get('consumer_secret') or conf['consumer_secret']

    key = kwargs.get('key') or conf['key']
    secret = kwargs.get('secret') or conf['secret']

    auth = tweepy.OAuthHandler(consumer_key=consumer_key, consumer_secret=consumer_secret)
    auth.set_access_token(key=key, secret=secret)

    return auth


class API(tweepy.API):

    '''Extends the tweepy API with config-file handling'''

    _app_name, _screen_name = None, None

    _config, _user_conf, _app_conf = {}, {}, {}

    _last_tweet, _last_reply, _last_retweet = None, None, None

    def __init__(self, screen_name, parsed_args=None, **kwargs):
        # Optionally used args from argparse.ArgumentParser
        if parsed_args:
            try:
                args = dict((k, v) for k, v in vars(parsed_args).items() if v is not None)
                kwargs.update(**args)
            except TypeError:
                # probably didn't get a Namespace() for passed args
                pass

        self._screen_name = screen_name

        # get config file and parse it

        # Use passed config file, or look for it in the paths above
        file_name = _find_config_file(kwargs.get('config'))
        file_config = helpers.config_parse(file_name)

        # kwargs take precendence over config file
        file_config.update(**kwargs)

        # set overall, app and user conf dicts
        conf = _config_setup(self, file_config)

        # setup auth
        try:
            auth = _setup_auth(conf, **kwargs)

        except KeyError:
            raise KeyError("Incomplete config")

        # initiate api connection
        super(API, self).__init__(auth)

    def update_config(self, update):
        self._config.update({k: v for k, v in update.items() if k not in PROTECTED_INFO})

    @property
    def config(self):
        return self._config

    @property
    def screen_name(self):
        return self._screen_name

    @property
    def app(self):
        return self._config['app']

    @property
    def last_tweet(self, refresh=None):
        if refresh or not self._last_tweet:
            self._last_tweet = self.user_timeline().pop(0).id

        return self._last_tweet

    @property
    def last_reply(self, refresh=None):
        if refresh or not self._last_reply:
            tl = self.user_timeline()
            filtered = [tweet for tweet in tl if tweet.in_reply_to_user_id]
            self._last_reply = filtered[0].id

        return self._last_reply

    @property
    def last_retweet(self, refresh=None):
        if refresh or not self._last_retweet:
            tl = self.user_timeline()
            filtered = [tweet for tweet in tl if tweet.retweeted]
            self._last_retweet = filtered[0].id

        return self._last_retweet

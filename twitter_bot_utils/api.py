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
from . import confighelper

CONFIG_DIRS = [
    '~',
    '~/bots',
]

CONFIG_BASES = [
    'botrc',
    'bots.yaml',
    'bots.json'
]


class API(tweepy.API):

    '''Extends the tweepy API with config-file handling'''

    _last_tweet, _last_reply, _last_retweet = None, None, None

    def __init__(self, screen_name, parsed_args=None, **kwargs):
        # Optionally used args from argparse.ArgumentParser
        if parsed_args:
            try:
                args = dict((k, v) for k, v in list(vars(parsed_args).items()) if v is not None)
                kwargs.update(**args)
            except TypeError:
                # probably didn't get a Namespace() for passed args
                pass

        self._screen_name = screen_name

        try:
            # get config file and parse it
            self._config, keys = confighelper.configure(screen_name, kwargs.get('config'), CONFIG_DIRS, CONFIG_BASES, **kwargs)

            # setup auth
            auth = confighelper.setup_auth(keys)

        except KeyError:
            raise ValueError("Incomplete config file.")

        # initiate api connection
        super(API, self).__init__(auth)

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

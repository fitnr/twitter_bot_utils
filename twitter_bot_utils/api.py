# Copyright 2014-16-16 Neil Freeman
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

from time import sleep
from argparse import Namespace
import logging
import tweepy
from .confighelper import configure
from . import args as tbu_args

PROTECTED_INFO = [
    'consumer_key',
    'consumer_secret',
    'key',
    'secret',
]


class API(tweepy.API):

    '''
    Extends the tweepy API with config-file handling.

    Args:
        args (Namespace): argparse.Namespace to read.
        screen_name (str): Twitter screen name
        config_file (str): Config file. Defaults to bots.json or bots.yaml in ~/ or ~/bots/.
        logger_name (str): Use a logger with this name. Defaults to screen_name
        format (str): Format for logger. Defaults to 'file lineno: message'
        verbose (bool): Set logging level to DEBUG
        quiet (bool): Set logging level to ERROR. Overrides verbose.
        kwargs: Other settings will be passed to the config
    '''

    _last_tweet = _last_reply = _last_retweet = None

    def __init__(self, args=None, **kwargs):
        '''
        Construct the tbu.API object.

        '''
        # Update the kwargs with contents of args
        if isinstance(args, Namespace):
            kwargs.update(vars(args))

        self._screen_name = kwargs.pop('screen_name', None)

        # Add a logger
        level = logging.DEBUG if kwargs.pop('verbose', None) else None
        level = logging.ERROR if kwargs.get('quiet', None) else level
        self.logger = tbu_args.add_logger(kwargs.pop('logger_name', self._screen_name), level,
                                          kwargs.pop('format', None))

        # get config file and parse it
        config = configure(self._screen_name, **kwargs)
        self._config = {k: v for k, v in config.items() if k not in PROTECTED_INFO}
        keys = {k: v for k, v in config.items() if k in PROTECTED_INFO}

        try:
            # setup auth
            auth = tweepy.OAuthHandler(consumer_key=keys['consumer_key'], consumer_secret=keys['consumer_secret'])

            try:
                auth.set_access_token(key=keys['key'], secret=keys['secret'])

            except KeyError:
                # API won't have an access key
                pass

        except KeyError:
            missing = [p for p in PROTECTED_INFO if p not in keys]
            raise ValueError("Incomplete config. Missing {}".format(missing))

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

    def _sinces(self):
        tl = self.user_timeline(self.screen_name, count=1000, include_rts=True, exclude_replies=False)

        if len(tl) > 0:
            self._last_tweet = tl[0].id
        else:
            self._last_tweet = self._last_reply = self._last_retweet = None
            return

        try:
            self._last_reply = max(t.id for t in tl if t.in_reply_to_user_id)
        except ValueError:
            self._last_reply = None

        try:
            self._last_retweet = max(t.id for t in tl if t.retweeted)
        except ValueError:
            self._last_retweet = None

    def _last(self, last_what, refresh):
        if refresh or getattr(self, last_what) is None:
            self._sinces()

        return getattr(self, last_what)

    @property
    def last_tweet(self, refresh=None):
        return self._last('_last_tweet', refresh)

    @property
    def last_reply(self, refresh=None):
        return self._last('_last_reply', refresh)

    @property
    def last_retweet(self, refresh=None):
        return self._last('_last_retweet', refresh)

    def update_status(self, *pargs, **kwargs):
        """
        Wrapper for tweepy.api.update_status with a 10s wait when twitter is over capacity
        """
        try:
            super(API, self).update_status(*pargs, **kwargs)

        except tweepy.TweepError as e:
            if getattr(e, 'api_code', None) == 503:
                sleep(10)
                super(API, self).update_status(*pargs, **kwargs)
            else:
                raise e

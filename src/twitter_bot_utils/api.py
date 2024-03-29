# -*- coding: utf-8 -*-
# Copyright 2014-2020 Neil Freeman
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

""" Wrapper around the tweepy.API """

import logging
import os
from argparse import Namespace

import tweepy

from . import args as tbu_args
from .confighelper import configure

PROTECTED_INFO = [
    "consumer_key",
    "consumer_secret",
    "key",
    "token",
    "oauth_token",
    "secret",
    "oauth_secret",
]


class API(tweepy.API):

    """
    Extends the tweepy API with config-file handling.

    Args:
        args (Namespace): argparse.Namespace to read.
        screen_name (str): Twitter screen name
        config_file (str): Config file. When False, don't read any config files.
            Defaults to bots.json or bots.yaml in ~/ or ~/bots/.
        logger_name (str): Use a logger with this name. Defaults to screen_name
        format (str): Format for logger. Defaults to 'file lineno: message'
        verbose (bool): Set logging level to DEBUG
        quiet (bool): Set logging level to ERROR. Overrides verbose.
        kwargs: Other settings will be passed to the config
    """

    def __init__(self, args=None, **kwargs):
        """
        Construct the tbu.API object.
        """
        # Update the kwargs with non-None contents of args
        if isinstance(args, Namespace):
            kwargs.update({k: v for k, v in vars(args).items() if v is not None})

        self._screen_name = kwargs.pop("screen_name", None)

        # Add a logger
        level = logging.DEBUG if kwargs.pop("verbose", None) else None
        level = logging.ERROR if kwargs.get("quiet", None) else level
        self.logger = tbu_args.add_logger(
            kwargs.pop("logger_name", self._screen_name),
            level,
            kwargs.pop("format", None),
        )

        # get config file and parse it
        config = configure(self._screen_name, **kwargs)
        self._config = {k: v for k, v in config.items() if k not in PROTECTED_INFO}
        keys = {k: v for k, v in config.items() if k in PROTECTED_INFO}

        try:
            # set up auth
            auth = tweepy.OAuth1UserHandler(
                consumer_key=keys["consumer_key"],
                consumer_secret=keys["consumer_secret"],
                access_token=keys.get("token", keys.get("key", keys.get("oauth_token"))),
                access_token_secret=keys.get("secret", keys.get("oauth_secret")),
            )
        except KeyError as err:
            missing = [p for p in PROTECTED_INFO if p not in keys]
            raise ValueError(f"Incomplete config. Missing {missing}") from err

        self._last_tweet = None
        self._last_reply = None
        self._last_retweet = None

        # initiate api connection
        super().__init__(auth)

    @property
    def config(self):
        """Return config dict."""
        return self._config

    @property
    def screen_name(self):
        """Return authorized @screen_name"""
        return self._screen_name

    @property
    def app(self):
        """Return current app name."""
        return self._config["app"]

    def _sinces(self):
        timeline = self.user_timeline(screen_name=self.screen_name, count=1000, include_rts=True, exclude_replies=False)

        if timeline:
            self._last_tweet = timeline[0].id
        else:
            self._last_tweet = self._last_reply = self._last_retweet = None
            return

        try:
            self._last_reply = max(t.id for t in timeline if t.in_reply_to_user_id)
        except ValueError:
            self._last_reply = None

        try:
            self._last_retweet = max(t.id for t in timeline if t.retweeted)
        except ValueError:
            self._last_retweet = None

    def _last(self, last_what, refresh=None):
        if refresh or getattr(self, last_what) is None:
            self._sinces()

        return getattr(self, last_what)

    @property
    def last_tweet(self):
        """Return most recent sent tweet."""
        return self._last("_last_tweet")

    @property
    def last_reply(self):
        """Return most recent sent reply."""
        return self._last("_last_reply")

    @property
    def last_retweet(self):
        """Return most recent retweet."""
        return self._last("_last_retweet")

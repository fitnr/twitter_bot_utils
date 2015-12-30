#!/usr/bin/env python
import os
import argparse
try:
    FileNotFoundError
except NameError:
    from errno import ENOENT
    FileNotFoundError = lambda x: IOError(ENOENT, x)

import unittest
import mock
import tweepy
from twitter_bot_utils import tools, API
from .test_api import fake_timeline

FAKE_FOLLOWERS_IDS = [1, 2, 3, 4]
FAKE_FRIENDS_IDS = [2, 3, 4, 5]

class testTools(unittest.TestCase):

    def setUp(self):
        self.yaml = os.path.join(os.path.dirname(__file__), 'data', 'test.yaml')

        self.args = argparse.Namespace(
            screen_name='example_screen_name',
            dry_run=True,
            verbose=False,
            quiet=True,
            config_file=self.yaml,
        )
        self.api = API(self.args)

    @mock.patch.object(tweepy.API, 'followers_ids', return_value=FAKE_FOLLOWERS_IDS)
    @mock.patch.object(tweepy.API, 'friends_ids', return_value=FAKE_FRIENDS_IDS)
    @mock.patch.object(tweepy.API, 'create_friendship', return_value=None)
    def testAutofollow(self, *_):
        tools.follow_back(self.api)

    @mock.patch.object(tweepy.API, 'followers_ids', return_value=FAKE_FOLLOWERS_IDS)
    @mock.patch.object(tweepy.API, 'friends_ids', return_value=FAKE_FRIENDS_IDS)
    @mock.patch.object(tweepy.API, 'destroy_friendship', return_value=None)
    def testAutoUnfollow(self, *_):
        tools.unfollow(self.api)

    @mock.patch.object(tweepy.API, 'mentions_timeline', return_value=fake_timeline())
    @mock.patch.object(tweepy.API, 'favorites', return_value=fake_timeline()[:2])
    @mock.patch.object(tweepy.API, 'create_favorite', return_value=None)
    def testFaveMentions(self, *_):
        tools.fave_mentions(self.api)

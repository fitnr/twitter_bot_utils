#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import unittest
import argparse
try:
    FileNotFoundError
except NameError:
    from errno import ENOENT
    FileNotFoundError = lambda x: IOError(ENOENT, x)

import vcr
import tweepy
from twitter_bot_utils import api, confighelper
from .config import credentials

class test_twitter_bot_utils(unittest.TestCase):

    @vcr.use_cassette('tests/fixtures/auth.yaml')
    def setUp(self):
        self.api = tweepy.API()

        self.yaml = os.path.join(os.path.dirname(__file__), 'data', 'test.yaml')
        self.json = os.path.join(os.path.dirname(__file__), 'data', 'test.json')
        self.simple = os.path.join(os.path.dirname(__file__), 'data', 'simple.yml')

        self.screen_name = credentials['screen_name']

        self.args = argparse.Namespace(
            screen_name=self.screen_name,
            dry_run=True,
            verbose=True,
            config_file=self.yaml,
        )

        self.txtfile = os.path.join(os.path.dirname(__file__), 'data', 'tweets.txt')
        self.archive = os.path.dirname(__file__)

    def test_api_creation_kws(self):
        twitter = api.API(**vars(self.args))
        assert isinstance(twitter, api.API)

    def test_api_creation_ns(self):
        twitter = api.API(self.args, config_file=self.yaml)
        assert isinstance(twitter, api.API)

    def test_api_missing_config(self):
        # Missing file raises IO Error
        self.assertRaises(IOError, api.API, 'example', config_file='dfV35d/does/not/exist/982')

    def test_api_broken_config(self):
        brokenconfig = os.path.join(os.path.dirname(__file__), 'data', 'broken.yaml')

        # Broken file raises ValueError
        self.assertRaises(ValueError, api.API, 'example_screen_name', config_file=brokenconfig)

    def test_api_environ_vars(self):
        os.environ['TWITTER_CONSUMER_KEY'] = 'value1'
        os.environ['TWITTER_CONSUMER_SECRET'] = 'value2'
        os.environ['TWITTER_KEY'] = 'value3'
        os.environ['TWITTER_SECRET'] = 'value4'

        twitter = api.API(screen_name='fake', config_file='.travis.yml')

        # Strange that two of these are bytes and two are str.
        self.assertEqual(twitter.auth.consumer_key.decode('utf8'), os.environ['TWITTER_CONSUMER_KEY'])
        assert twitter.auth.consumer_secret.decode('utf8') == os.environ['TWITTER_CONSUMER_SECRET']
        assert twitter.auth.access_token == os.environ['TWITTER_KEY']
        assert twitter.auth.access_token_secret == os.environ['TWITTER_SECRET']

    def test_api_attributes(self):
        twitter = api.API(**vars(self.args))
        self.assertEqual(twitter.config['custom'], 'user')

        try:
            key = twitter.config['key']
        except KeyError:
            key = False

        assert key is False

        assert twitter.screen_name == 'example_screen_name'
        assert twitter.app == 'example_app_name'

    def testApiAttributesNamespace(self):
        twitter = api.API(self.args)

        assert twitter.config['custom'] == 'user'
        assert twitter.screen_name == 'example_screen_name'
        assert twitter.app == 'example_app_name'

    @vcr.use_cassette('tests/fixtures/user_timeline.yaml')
    def test_recent_tweets(self):
        twitter = api.API(self.args)

        self.assertEqual(twitter.last_tweet, 1235)
        assert twitter.last_retweet == 1233
        assert twitter.last_reply == 1234

    @vcr.use_cassette('tests/fixtures/status.yaml')
    def test_user_status(self):
        twitter = api.API(self.args)
        mock_status = TIMELINE[0]

        status1 = super(api.API, twitter).update_status(text=mock_status['text'])
        self.assertIsNotNone(status1)

        status = twitter.update_status(text=mock_status['text'])
        self.assertIsNotNone(status, 'Returned status object is None')

        assert status.id == mock_status['id']
        assert status.text == mock_status['text']

    @vcr.use_cassette('tests/fixtures/user_timeline.yaml')
    def test_recent_tweets_no_rts(self, _):
        twitter = api.API(self.args)

        self.assertEqual(twitter.last_tweet, 1235)
        assert twitter.last_retweet is None
        assert twitter.last_reply is None

    @vcr.use_cassette('tests/fixtures/set_access_token.yaml')
    def testSetupAuth(self, *_):
        auth = confighelper.setup_auth(**credentials)
        assert isinstance(auth, tweepy.OAuthHandler)


if __name__ == '__main__':
    unittest.main()

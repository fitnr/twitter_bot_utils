#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import os
import unittest

import tweepy
from vcr import VCR

from twitter_bot_utils import api, confighelper

from .config import credentials

vcr = VCR(filter_headers=['Authorization'])


class test_twitter_bot_utils(unittest.TestCase):
    # pylint: disable=invalid-name
    _api = None

    def setUp(self):
        self.yaml = os.path.join(os.path.dirname(__file__), 'data', 'test.yaml')
        self.json = os.path.join(os.path.dirname(__file__), 'data', 'test.json')
        self.simple = os.path.join(os.path.dirname(__file__), 'data', 'simple.yml')
        self.txtfile = os.path.join(os.path.dirname(__file__), 'data', 'tweets.txt')
        self.archive = os.path.dirname(__file__)

    @vcr.use_cassette('tests/fixtures/verify_credentials.yaml')
    def api(self):
        if not self._api:
            self._api = api.API(config_file=False, **credentials)
            self.assertEqual(self._api.screen_name, credentials['screen_name'])
            self.assertEqual(self._api.auth.get_username(), credentials['screen_name'])

        return self._api

    def testApiSetup(self):
        self.api()

    def test_api_creation_ns(self):
        args = argparse.Namespace(**credentials)
        twitter = api.API(args, config_file=self.yaml)
        assert isinstance(twitter, api.API)

    def test_api_missing_config(self):
        # Missing file raises IO Error
        self.assertRaises(IOError, api.API, 'example', config_file='dfV35d/does/not/exist/982')

    def test_api_broken_config(self):
        brokenconfig = os.path.join(os.path.dirname(__file__), 'data', 'broken.yaml')

        # Broken file raises ValueError
        self.assertRaises(ValueError, api.API, use_env=False, config_file=brokenconfig)

    def testEnviron(self):
        twitter = self.api()
        self.assertEqual(twitter.screen_name, credentials['screen_name'])
        self.assertEqual(twitter.auth.consumer_key.decode('utf8'), credentials['consumer_key'])
        self.assertEqual(twitter.auth.consumer_secret.decode('utf8'), credentials['consumer_secret'])
        self.assertEqual(twitter.auth.access_token, credentials['token'])
        self.assertEqual(twitter.auth.access_token_secret, credentials['secret'])

    def testApiAttributes(self):
        twitter = api.API(screen_name='example_screen_name', config_file=self.yaml, use_env=False)

        assert twitter.config['custom'] == 'user'
        assert twitter.screen_name == 'example_screen_name'
        assert twitter.app == 'example_app_name'

    @vcr.use_cassette('tests/fixtures/user_timeline.yaml')
    def test_recent_tweets(self):
        twitter = self.api()
        self.assertEqual(twitter.last_tweet, 936319185277341697)

    @vcr.use_cassette('tests/fixtures/status.yaml')
    def test_user_status(self):
        twitter = self.api()

        status1 = super(api.API, twitter).update_status("Just running some tests...")
        self.assertIsNotNone(status1)
        assert status1.text == "Just running some tests..."

        status = twitter.update_status("Just running some more tests...")
        self.assertIsNotNone(status, 'Returned status object is None')
        assert status.text == "Just running some more tests..."

    def testSetupAuth(self):
        auth = confighelper.setup_auth(**credentials)
        self.assertIsInstance(auth, tweepy.OAuthHandler)


if __name__ == '__main__':
    unittest.main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
from twitter_bot_utils import api, confighelper

TIMELINE = [
    {
        "id": 1235,
        "id_str": "1235",
        "in_reply_to_user_id": None,
        "retweeted": False,
        "text": "Asperiores libero distinctio cum laboriosam."
    },
    {
        "id": 1234,
        "id_str": "1234",
        "in_reply_to_user_id": 1,
        "retweeted": False,
        "text": "consectetur adipisicing elit"
    },
    {
        "id": 1233,
        "id_str": "1233",
        "retweeted": True,
        "in_reply_to_user_id": None,
        "text": "Lorem ipsum dolor sit amet"
    },
]


def fake_timeline():
    return [tweepy.Status.parse(tweepy.api, t) for t in TIMELINE]


class test_twitter_bot_utils(unittest.TestCase):

    def setUp(self):
        self.api = tweepy.API()

        self.yaml = os.path.join(os.path.dirname(__file__), 'data', 'test.yaml')
        self.json = os.path.join(os.path.dirname(__file__), 'data', 'test.json')
        self.simple = os.path.join(os.path.dirname(__file__), 'data', 'simple.yml')

        self.screen_name = 'example_screen_name'

        self.args = argparse.Namespace(
            screen_name='example_screen_name',
            dry_run=True,
            verbose=True,
            config_file=self.yaml,
        )

        self.txtfile = os.path.join(os.path.dirname(__file__), 'data', 'tweets.txt')
        self.archive = os.path.dirname(__file__)

    def testDefaultDirs(self):
        assert '~' in confighelper.CONFIG_DIRS

    def testConfigKwargPassing(self):
        conf = confighelper.parse(self.yaml)
        config = confighelper.configure(config_file=self.yaml, **conf)
        assert conf['custom'] == config['custom']

    def testConfigKwargPassingJSON(self):
        conf = confighelper.parse(self.json)
        config = confighelper.configure(config_file=self.json, **conf)
        assert conf['custom'] == config['custom']

    def testConfigBadFileType(self):
        with self.assertRaises(ValueError):
            confighelper.parse(self.txtfile)

    def testDumpConfig(self):
        conf = confighelper.parse(self.json)
        sink = 'a.json'
        confighelper.dump(conf, sink)

        dumped = confighelper.parse(sink)

        assert dumped['custom'] == conf['custom']
        assert 'users' in dumped

        os.remove(sink)

    def testDumpConfigBadFileType(self):
        with self.assertRaises(ValueError):
            confighelper.dump({}, 'foo.whatever')

    def testMissingConfig(self):
        with self.assertRaises(Exception):
            confighelper.find_file('imaginary.yaml', (os.path.dirname(__file__),))

    def test_config_setup(self):
        config = confighelper.configure(self.screen_name, config_file=self.yaml, random='foo')

        assert config['secret'] == 'LIMA'
        assert config['consumer_key'] == 'NOVEMBER'
        assert config['random'] == 'foo'

    def testSimpleConfig(self):
        config = confighelper.configure(config_file=self.simple, random='foo')
        assert config['secret'] == 'LIMA'
        assert config['consumer_key'] == 'NOVEMBER'
        assert config['random'] == 'foo'

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

    @mock.patch.object(tweepy.API, 'user_timeline', return_value=fake_timeline())
    def test_recent_tweets(self, _):

        twitter = api.API(self.args)

        self.assertEqual(twitter.last_tweet, 1235)
        assert twitter.last_retweet == 1233
        assert twitter.last_reply == 1234

    @mock.patch.object(tweepy.API, 'user_timeline', return_value=[fake_timeline()[0]])
    def test_recent_tweets_no_rts(self, _):
        twitter = api.API(self.args)

        self.assertEqual(twitter.last_tweet, 1235)
        assert twitter.last_retweet is None
        assert twitter.last_reply is None

    @mock.patch.object(tweepy.OAuthHandler, 'set_access_token')
    def testSetupAuth(self, *_):
        keys = {
            "consumer_key": 'AAA',
            "consumer_secret": "BBB",
            "key": "CCC",
            "secret": "DDD"
        }

        auth = confighelper.setup_auth(**keys)
        assert isinstance(auth, tweepy.OAuthHandler)

if __name__ == '__main__':
    unittest.main()

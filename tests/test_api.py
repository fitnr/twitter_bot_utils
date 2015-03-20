import os
import unittest
import tweepy
import argparse
from twitter_bot_utils import api, confighelper


class test_twitter_bot_utils(unittest.TestCase):

    def setUp(self):
        self.api = tweepy.API()

        self.yaml = os.path.join(os.path.dirname(__file__), 'data/test.yaml')

        self.screen_name = 'example_screen_name'

        self.args = argparse.Namespace()
        setattr(self.args, 'consumer-key', '123')
        setattr(self.args, 'dry_run', True)
        setattr(self.args, 'verbose', True)

        self.txtfile = os.path.join(os.path.dirname(__file__), 'data/tweets.txt')
        self.archive = os.path.dirname(__file__)

    def test_config_setup(self):
        fileconfig = confighelper.parse(self.yaml)
        config, keys = confighelper.setup(self.screen_name, fileconfig)

        assert config['custom'] == 'foo'
        assert keys['secret'] == 'LIMA'
        assert keys['consumer_key'] == 'NOVEMBER'

    def test_update_config(self):
        a = {'foo': 'bar'}
        b = {'foo': 'mux', 'key': 'a'}
        confighelper.update(a, b)

        self.assertEqual(a['foo'], b['foo'])
        self.assertIsNone(a.get('key'))

    def test_api_creation(self):
        twitter = api.API('example_screen_name', config_file=self.yaml, **vars(self.args))

        assert isinstance(twitter, api.API)

    def test_api_args(self):
        brokenconfig = os.path.join(os.path.dirname(__file__), 'data/broken.yaml')

        self.assertRaises(ValueError, api.API, 'example')
        self.assertRaises(ValueError, api.API, 'example_screen_name', config_file=brokenconfig)

    def test_api_attributes(self):
        twitter = api.API('example_screen_name', config_file=self.yaml, **vars(self.args))

        assert twitter.config['custom'] == 'foo'

        try:
            key = twitter.config['key']
        except KeyError:
            key = False

        assert key is False

        assert twitter.screen_name == 'example_screen_name'
        assert twitter.app == 'example_app_name'

if __name__ == '__main__':
    unittest.main()

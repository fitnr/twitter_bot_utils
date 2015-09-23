import os
import unittest
import mock
import tweepy
import argparse
from twitter_bot_utils import api, confighelper

TIMELINE = [
    {
        "id": 1235,
        "in_reply_to_user_id": None,
        "retweeted": False
    },
    {
        "id": 1234,
        "in_reply_to_user_id": 1,
        "retweeted": False
    },
    {
        "id": 1233,
        "retweeted": True,
        "in_reply_to_user_id": None,
    },
]


def fake_timeline():
    return [tweepy.Status.parse(tweepy.api, t) for t in TIMELINE]


class test_twitter_bot_utils(unittest.TestCase):

    def setUp(self):
        self.api = tweepy.API()

        self.yaml = os.path.join(os.path.dirname(__file__), 'data', 'test.yaml')

        self.screen_name = 'example_screen_name'

        self.args = argparse.Namespace()
        setattr(self.args, 'consumer-key', '123')
        setattr(self.args, 'dry_run', True)
        setattr(self.args, 'verbose', True)

        self.txtfile = os.path.join(os.path.dirname(__file__), 'data', 'tweets.txt')
        self.archive = os.path.dirname(__file__)

    def test_config_setup(self):
        fileconfig = confighelper.parse(self.yaml)
        config, keys = confighelper.setup(fileconfig, self.screen_name)

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

    def test_api_missing_config(self):
        # Missing file raises IO Error
        self.assertRaises(IOError, api.API, 'example')

    def test_api_broken_config(self):
        brokenconfig = os.path.join(os.path.dirname(__file__), 'data', 'broken.yaml')

        # Broken file raises ValueError
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

    @mock.patch.object(tweepy.API, 'user_timeline', return_value=fake_timeline())
    def test_recent_tweets(self, _):

        twitter = api.API('example_screen_name', config_file=self.yaml, **vars(self.args))

        self.assertEqual(twitter.last_tweet, 1235)
        assert twitter.last_retweet == 1233
        assert twitter.last_reply == 1234

    @mock.patch.object(tweepy.API, 'user_timeline', return_value=[fake_timeline()[0]])
    def test_recent_tweets_no_rts(self, _):

        twitter = api.API('example_screen_name', config_file=self.yaml, **vars(self.args))

        self.assertEqual(twitter.last_tweet, 1235)
        assert twitter.last_retweet is None
        assert twitter.last_reply is None

    @mock.patch.object(tweepy.API, 'user_timeline', return_value=[])
    def test_recent_tweets_no_tl(self, _):

        twitter = api.API('example_screen_name', config_file=self.yaml, **vars(self.args))

        self.assertEqual(twitter.last_tweet, None)
        assert twitter.last_retweet is None
        assert twitter.last_reply is None


if __name__ == '__main__':
    unittest.main()

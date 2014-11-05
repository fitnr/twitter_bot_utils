import os
import unittest
import tweepy
import logging
import argparse
from twitter_bot_utils import api, creation, helpers, tools

TWEET = {
    "source": "\u003Ca href=\"http:\/\/twitter.com\/download\/iphone\" rel=\"nofollow\"\u003ETwitter for iPhone\u003C\/a\u003E",
    "entities": {
        "user_mentions": [{
            "name": "John Doe",
            "screen_name": "twitter",
            "indices": [0, 8],
            "id_str": "1",
            "id": 1
        }],
        "media": [],
        "hashtags": [],
        "urls": []
    },
    "in_reply_to_status_id_str": "318563540590010368",
    "id_str": "318565861172600832",
    "in_reply_to_user_id": 14155645,
    "text": "@twitter example tweet example tweet example tweet",
    "id": 318565861172600832,
    "in_reply_to_status_id": 318563540590010368,
    "in_reply_to_screen_name": "twitter",
    "in_reply_to_user_id_str": "14155645",
    "retweeted": None,
    "user": {
        "name": "Neil Freeman",
        "screen_name": "fitnr",
        "protected": False,
        "id_str": "6853512",
        "profile_image_url_https": "https:\/\/pbs.twimg.com\/profile_images\/431817496350314496\/VGgzYAE7_normal.jpeg",
        "id": 6853512,
        "verified": False
    }
}


class test_twitter_bot_utils(unittest.TestCase):

    def setUp(self):
        self.api = tweepy.API()
        self.status = tweepy.Status.parse(self.api, TWEET)

        self.yaml = os.path.join(os.path.dirname(__file__), 'test.yaml')
        self.parser = creation.setup_args(description='desc')

        self.arg_input = ['--consumer-key', '123', '-n', '-v']
        self.args = self.parser.parse_args(self.arg_input)

    def test_setup(self):

        assert isinstance(self.parser, argparse.ArgumentParser)
        assert self.parser.description == 'desc'

    def test_parsing_args(self):
        args = self.parser.parse_args(self.arg_input)

        assert args.consumer_key == '123'
        assert args.config is None
        assert args.dry_run
        assert args.verbose

    def test_creation_defaults(self):
        args = self.parser.parse_args(self.arg_input)

        creation.defaults('test', args)

        l = logging.getLogger('test')
        assert isinstance(l, logging.Logger)

        assert l.name == 'test'

        assert len(l.handlers) == 2
        assert isinstance(l.handlers[1], logging.StreamHandler)

    def test_helpers(self):
        assert helpers.has_hashtag(self.status) is False
        assert helpers.has_mention(self.status)

        assert helpers.remove_entity(self.status, 'hashtags') == self.status.text
        assert helpers.remove_entity(self.status, 'user_mentions') == " example tweet example tweet example tweet"
        assert helpers.remove_entities(self.status, ['hashtags', 'user_mentions']) == " example tweet example tweet example tweet"

    def test_api_conf_file(self):
        assert api._find_config_file(self.yaml) == self.yaml

    def test_api_creation(self):
        twitter = api.API('example_screen_name', self.args, config=self.yaml)

        assert isinstance(twitter, api.API)

    def test_api_attributes(self):
        twitter = api.API('example_screen_name', self.args, config=self.yaml)

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

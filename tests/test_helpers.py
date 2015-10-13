# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import unittest
import tweepy
from twitter_bot_utils import helpers

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


class test_tbu_helpers(unittest.TestCase):

    def setUp(self):
        self.api = tweepy.API()
        self.status = tweepy.Status.parse(self.api, TWEET)

    def test_has_entities(self):
        assert helpers.has_entities(self.status) is True

    def test_has_hashtag(self):
        assert helpers.has_hashtag(self.status) is False

    def test_has_mention(self):
        assert helpers.has_mention(self.status)

    def test_remove_entities(self):
        assert helpers.remove_entity(self.status, 'hashtags') == self.status.text
        assert helpers.remove_entity(
            self.status, 'user_mentions') == " example tweet example tweet example tweet"
        assert helpers.remove_entities(
            self.status, ['hashtags', 'user_mentions']) == " example tweet example tweet example tweet"

    def test_replace_urls(self):
        assert helpers.replace_urls(self.status) == TWEET['text']

        TWEET['entities']['urls'] = [{"indices": [0, 12], "expanded_url": "http://long.long.url"}]
        TWEET['text'] = 'http://short hey'

        status = tweepy.Status.parse(self.api, TWEET)

        assert helpers.replace_urls(status) == "http://long.long.url hey"

    def test_shorten(self):
        hello = ("This is a long string that's longer than 140 characters, "
                 "yes it's quite long. It's so long that we need to shorten it. "
                 "Supercalifragilisticexpialidocious! Amazing. I want to test this.")

        for l in range(10, 180, 10):
            self.assertLessEqual(len(helpers.shorten(hello, l)), l)

        assert helpers.shorten(hello, ellipsis=True)[-1:] == '…'
        assert helpers.shorten(hello, ellipsis='...')[-3:] == '...'

        assert helpers.shorten('hello') == 'hello'
        assert helpers.shorten(hello, 500) == hello

        assert helpers.shorten(hello, ellipsis=True) == (
            "This is a long string that's longer than 140 characters, "
            "yes it's quite long. It's so long that we need to shorten it…")

    def test_querize(self):
        query = ('hi', 'bye', 'wow', '-no', '-nah')
        self.assertEqual(helpers.queryize(query), 'hi+OR+bye+OR+wow+-no+-nah')
        self.assertEqual(helpers.queryize(query, 'user'), 'hi+OR+bye+OR+wow+-from%3Auser+-no+-nah')

if __name__ == '__main__':
    unittest.main()

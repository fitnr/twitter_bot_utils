#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest

import tweepy

from twitter_bot_utils import helpers

from .config import example_tweet


class test_tbu_helpers(unittest.TestCase):
    # pylint: disable=invalid-name
    def setUp(self):
        self.api = tweepy.API()
        self.tweet = example_tweet
        self.status = tweepy.Status.parse(self.api, self.tweet)

    def test_has_entities(self):
        assert helpers.has_entities(self.status) is True
        assert helpers.has_entities(self.tweet) is True

        assert helpers.has_media(self.tweet) is False
        assert helpers.has_media(self.status) is False

        assert helpers.has_symbol(self.status) is False
        assert helpers.has_symbol(self.tweet) is False

    def test_has_hashtag(self):
        assert helpers.has_hashtag(self.status) is False
        assert helpers.has_hashtag(self.tweet) is False

    def test_has_mention(self):
        assert helpers.has_mention(self.status)
        assert helpers.has_mention(self.tweet)

    def test_remove_entities(self):
        assert helpers.remove_entity(self.status, 'hashtags') == self.status.text
        assert helpers.remove_entity(self.status, 'user_mentions') == " example tweet example tweet example tweet"
        assert (
            helpers.remove_entities(self.status, ['hashtags', 'user_mentions'])
            == " example tweet example tweet example tweet"
        )
        assert (
            helpers.remove_entities(self.tweet, ['hashtags', 'user_mentions'])
            == " example tweet example tweet example tweet"
        )

    def test_replace_urls(self):
        assert helpers.replace_urls(self.status) == self.tweet['text']

        self.tweet['entities']['urls'] = [{"indices": [0, 12], "expanded_url": "http://long.long.url"}]
        self.tweet['text'] = 'http://short hey'

        status = tweepy.Status.parse(self.api, self.tweet)

        assert helpers.replace_urls(status) == "http://long.long.url hey"

    def test_shorten(self):
        hello = (
            "This is a long string that's longer than 140 characters, "
            "yes it's quite long. It's so long that we need to shorten it. "
            "Supercalifragilisticexpialidocious! Amazing. I want to test this."
        )

        for i in range(10, 180, 10):
            self.assertLessEqual(len(helpers.shorten(hello, i)), i)

        assert helpers.shorten(hello, ellipsis=True)[-1:] == '…'
        assert helpers.shorten(hello, ellipsis='...')[-3:] == '...'

        assert helpers.shorten('hello') == 'hello'
        assert helpers.shorten(hello, 500) == hello

        assert helpers.shorten(hello, ellipsis=True) == (
            "This is a long string that's longer than 140 characters, "
            "yes it's quite long. It's so long that we need to shorten it…"
        )

    def test_querize(self):
        query = ('hi', 'bye', 'oh wow', '-no', '-nuh uh')
        self.assertEqual(helpers.queryize(query).strip(), '"hi" OR "bye" OR "oh wow" -"no" -"nuh uh"')
        self.assertEqual(helpers.queryize(query, 'user'), '"hi" OR "bye" OR "oh wow" -"no" -"nuh uh" -from:user')

    def testLength(self):
        # equal len and length
        strings = [
            'happy 123',  # ascii
            u'ქართული ენა',  # Georgian
            u'˗˖˭ʰ',  # Spacing modifiers
            u'āz̪u̾ìì',  # diacretics
        ]
        for s in strings:
            self.assertEqual(len(s), helpers.length(s))

        # compare non-normalized with normalized forms
        self.assertEqual(helpers.length('café'), helpers.length('café'))

        # characters that count as "2"
        strings = [
            u'ᏣᎳᎩᎦᏬᏂᎯᏍᏗ',  # Cherokee language
            # Phonetic extensions
            ''.join(chr(x) for x in range(int('1D00', 16), int('1DBF', 16))),
            # generally a bunch of higher-level unicode
            ''.join(chr(x) for x in range(int('1100', 16), int('2F96C', 16), 200)),
        ]
        for s in strings:
            self.assertEqual(len(s) * 2, helpers.length(s))

        s = ''.join(x + y for x, y in zip(u'ᏣᎳᎩᎦᏬᏂᎯᏍᏗ', u'abcdefghi'))
        self.assertEqual(int(len(s) * 1.5), helpers.length(s))

    def testChomp(self):
        long_string = (
            "It was the best of times, it was the worst of times, "
            "it was the age of wisdom, it was the age of foolishness, "
            "it was the epoch of belief, it was the epoch of incredulity, "
            "it was the season of Light, it was the season of Darkness, "
            "it was the spring of hope, it was the winter of despair, "
            "we had everything before us, we had nothing before us, "
            "we were all going direct to Heaven, we were all going direct the other way— in short, "
            "the period was so far like the present period, "
            "that some of its noisiest authorities insisted on its being received, "
            "for good or for evil, in the superlative degree of comparison only."
        )

        chomp_140 = (
            "It was the best of times, it was the worst of times, it was the age of wisdom, "
            "it was the age of foolishness, it was the epoch of belief"
        )

        self.assertEqual(helpers.chomp(long_string, max_len=140), chomp_140)

        self.assertEqual(helpers.chomp(long_string, max_len=30), "It was the best of times")

        chomp_140_comma = (
            "It was the best of times, it was the worst of times, it was the age of wisdom, "
            "it was the age of foolishness, it was the epoch of belief, it"
        )

        self.assertEqual(helpers.chomp(long_string, split=' ,', max_len=140), chomp_140_comma)

        self.assertEqual(helpers.chomp(long_string, split='9'), long_string)


if __name__ == '__main__':
    unittest.main()

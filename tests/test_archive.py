#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import inspect
import os
import sys
import unittest

import tweepy

from twitter_bot_utils import archive, args, confighelper

from .config import example_tweet


class test_twitter_bot_utils(unittest.TestCase):
    # pylint: disable=invalid-name
    screen_name = 'example_screen_name'

    archive = os.path.dirname(__file__)
    csvfile = os.path.join(os.path.dirname(__file__), 'data', 'tweets.csv')
    txtfile = os.path.join(os.path.dirname(__file__), 'data', 'tweets.txt')
    yaml = os.path.join(os.path.dirname(__file__), 'data', 'test.yaml')

    def setUp(self):
        self.api = tweepy.API()
        self.status = tweepy.Status.parse(self.api, example_tweet)

        parent = args.parent(version='1.2.3')
        self.parser = argparse.ArgumentParser(description='desc', parents=[parent])

        sys.argv = ['test', '--dry-run', '-v', '-c', self.yaml]
        self.args = self.parser.parse_args()

    def test_setup(self):
        assert isinstance(self.parser, argparse.ArgumentParser)
        assert self.parser.description == 'desc'

    def test_parsing_args(self):
        assert self.args.dry_run
        assert self.args.verbose

    def test_find_conf_file(self):
        assert confighelper.find_file(self.yaml) == self.yaml
        real_path = os.path.realpath(os.path.dirname(__file__))

        self.assertEqual(
            confighelper.find_file(default_directories=[real_path], default_bases=[self.yaml]),
            os.path.realpath(self.yaml),
        )

    def test_parse(self):
        parsed = confighelper.parse(self.yaml)
        assert parsed['users']['example_screen_name']['key'] == 'INDIA'
        self.assertEqual(parsed['custom'], 'general')
        self.assertEqual(parsed['users']['example_screen_name']['custom'], 'user')

    def test_loading_archive_data(self):
        archives = archive.read_json(self.archive)
        assert inspect.isgenerator(archives)
        a = list(archives)
        self.assertEqual(len(a), 3)

        self.assertEqual(a[2]['text'], u"#ééé #buttons")

    def test_loading_csv_data(self):
        txt = archive.read_csv(self.csvfile)
        assert inspect.isgenerator(txt)
        tweets = list(txt)

        try:
            self.assertIsInstance(tweets[0]['text'], unicode)
            assert isinstance(tweets[4]['text'], unicode)
        except NameError:
            assert isinstance(tweets[0]['text'], str)
            assert isinstance(tweets[4]['text'], str)

        self.assertEqual(len(tweets), 6)
        self.assertEqual(tweets[4]['text'], u'Tweet with an åccent')
        self.assertEqual(tweets[5]['text'], u'Tweet with an 😀 emoji')

    def test_loading_text_data(self):
        txt = archive.read_text(self.txtfile)
        assert inspect.isgenerator(txt)
        tweets = list(txt)

        try:
            self.assertIsInstance(tweets[0], unicode)
            assert isinstance(tweets[4], unicode)
        except NameError:
            assert isinstance(tweets[0], str)
            assert isinstance(tweets[4], str)

        self.assertEqual(len(tweets), 6)
        self.assertEqual(tweets[4], u'Tweet with an åccent')
        self.assertEqual(tweets[5], u'Tweet with an 😀 emoji')


if __name__ == '__main__':
    unittest.main()

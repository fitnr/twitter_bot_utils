#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from vcr import VCR

from twitter_bot_utils import API, tools

from .config import credentials

vcr = VCR(filter_headers=['Authorization'])


class testTools(unittest.TestCase):
    # pylint: disable=invalid-name
    def setUp(self):
        self.api = API(config_file=False, **credentials)

    @vcr.use_cassette('tests/fixtures/followback.yaml')
    def testAutofollow(self):
        tools.follow_back(self.api, dry_run=True)

    @vcr.use_cassette('tests/fixtures/unfollow.yaml')
    def testAutoUnfollow(self):
        tools.unfollow(self.api, dry_run=True)

    @vcr.use_cassette('tests/fixtures/favorite.yaml')
    def testFaveMentions(self):
        tools.fave_mentions(self.api, dry_run=True)

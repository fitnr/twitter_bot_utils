#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
try:
    FileNotFoundError
except NameError:
    from errno import ENOENT
    FileNotFoundError = lambda x: IOError(ENOENT, x)

import unittest
import vcr
from twitter_bot_utils import tools, API
from .config import credentials

class testTools(unittest.TestCase):

    def setUp(self):
        self.yaml = os.path.join(os.path.dirname(__file__), 'data', 'test.yaml')
        self.api = API(**credentials)

    @vcr.use_cassette('tests/fixtures/followback.yaml')
    def testAutofollow(self, *_):
        tools.follow_back(self.api)

    @vcr.use_cassette('tests/fixtures/unfollow.yaml')
    def testAutoUnfollow(self, *_):
        tools.unfollow(self.api)

    @vcr.use_cassette('tests/fixtures/favorite.yaml')
    def testFaveMentions(self, *_):
        tools.fave_mentions(self.api)

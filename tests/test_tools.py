#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
try:
    FileNotFoundError
except NameError:
    from errno import ENOENT
    FileNotFoundError = lambda x: IOError(ENOENT, x)

import unittest
from vcr import VCR
from twitter_bot_utils import tools, API
from .config import credentials

vcr = VCR(filter_headers=['Authorization'])

class testTools(unittest.TestCase):

    def setUp(self):
        self.yaml = os.path.join(os.path.dirname(__file__), 'data', 'test.yaml')
        self.api = API(**credentials)

    @vcr.use_cassette('tests/fixtures/followback.yaml')
    def testAutofollow(self):
        tools.follow_back(self.api, dry_run=True)

    @vcr.use_cassette('tests/fixtures/unfollow.yaml')
    def testAutoUnfollow(self):
        tools.unfollow(self.api, dry_run=True)

    @vcr.use_cassette('tests/fixtures/favorite.yaml')
    def testFaveMentions(self):
        tools.fave_mentions(self.api, dry_run=True)

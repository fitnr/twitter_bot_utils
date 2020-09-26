#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import os.path
import unittest

from twitter_bot_utils import args


class test_twitter_bot_utils(unittest.TestCase):
    # pylint: disable=invalid-name
    def setUp(self):
        self.screen_name = 'example_screen_name'

        self.parser = argparse.ArgumentParser(description='desc', parents=[args.parent()])

        self.args = self.parser.parse_args(['-n', '-v'])

        self.txtfile = os.path.join(os.path.dirname(__file__), 'data', 'tweets.txt')
        self.archive = os.path.dirname(__file__)

    def test_args(self):
        assert self.args.dry_run is True
        assert self.args.verbose is True


if __name__ == '__main__':
    unittest.main()

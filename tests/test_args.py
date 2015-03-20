import os.path
import unittest
import argparse
from twitter_bot_utils import args


class test_twitter_bot_utils(unittest.TestCase):

    def setUp(self):
        self.screen_name = 'example_screen_name'

        self.parser = argparse.ArgumentParser(description='desc', parents=[args.parent()])

        self.args = self.parser.parse_args(['--consumer-key', '123', '-n', '-v'])

        self.txtfile = os.path.join(os.path.dirname(__file__), 'data/tweets.txt')
        self.archive = os.path.dirname(__file__)

    def test_args(self):
        assert self.args.consumer_key == '123'
        assert self.args.dry_run == True
        assert self.args.verbose == True

if __name__ == '__main__':
    unittest.main()

#!/usr/local/bin/python
import tweet_utils
import argparse

parser = argparse.ArgumentParser(description='fave mentions')
parser.add_argument('-u', '--screen_name', type=str, help='User who will be doing the favoriting')
parser.add_argument('-a', '--app', type=str, help='Name of the app to authenticate with')
args = parser.parse_args()

screen_name = args.screen_name
app = args.app

api = tweet_utils.utils.fave_mentions(app=app, screen_name=screen_name)
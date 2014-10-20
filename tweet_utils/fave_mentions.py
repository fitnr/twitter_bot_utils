#!/usr/local/bin/python
from tweet_utils import utils
import argparse


def main():
    parser = argparse.ArgumentParser(description='fave mentions')
    parser.add_argument('-u', '--screen_name', type=str, help='User who will be doing the favoriting')
    parser.add_argument('-a', '--app', type=str, help='Name of the app to authenticate with')
    args = parser.parse_args()

    screen_name = args.screen_name
    app = args.app

    utils.fave_mentions(app=app, screen_name=screen_name)

if __name__ == '__main__':
    main()

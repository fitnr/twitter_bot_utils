#!/usr/local/bin/python
from . import api
import argparse


def main():
    parser = argparse.ArgumentParser(description='fave mentions')
    parser.add_argument('-u', '--screen_name', type=str, help='User who will be doing the favoriting')
    parser.add_argument('-a', '--app', type=str, help='Name of the app to authenticate with')
    parser.add_argument('-c', '--api_config', type=str, help='(optional) file with api auth details')
    args = parser.parse_args()

    twitter = api.API(args.app, args.screen_name, args.api_config)
    twitter.fave_mentions()

if __name__ == '__main__':
    main()

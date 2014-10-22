#!/usr/local/bin/python
from . import api
import argparse


def fave_mentions():
    parser = argparse.ArgumentParser(description='fave mentions')
    parser.add_argument('-u', '--screen_name', type=str, help='User who will be doing the favoriting')
    parser.add_argument('-a', '--app', type=str, help='Name of the app to authenticate with')
    parser.add_argument('-c', '--api_config', type=str, help='(optional) file with api auth details')
    args = parser.parse_args()

    twitter = api.API(args.app, args.screen_name, args.api_config)
    twitter.fave_mentions()


def auto_follow():
    parser = argparse.ArgumentParser(description="automatic following")
    parser.add_argument('-u', '--screen_name', type=str, help='User who will be doing the favoriting')
    parser.add_argument('-a', '--app', type=str, help='Name of the app to authenticate with')
    parser.add_argument('-u', '--unfollow', action='store_true', help='Unfollow those who dont follow you')
    parser.add_argument('-c', '--api_config', type=str, help='(optional) file with api auth details')

    args = parser.parse_args()

    twitter = api.API(args.app, args.screen_name, args.api_config)

    if args.unfollow:
        twitter.unfollow()
    else:
        twitter.follow_back()

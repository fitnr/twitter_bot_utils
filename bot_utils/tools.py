#!/usr/local/bin/python
from . import api
import argparse
import yaml
import json

def no_entities(status):
    try:
        e = status.entities
    except AttributeError:
        return True
    if len(e['urls']) == 0 and len(e['hashtags']) == 0 and len(e['user_mentions']) == 0:
        return True
    else:
        return False

def clean_status(status):
    try:
        if no_entities(status) and status.metadata.get('iso_language_code') == 'en':
            return True
        else:
            return False
    except AttributeError:
        return False

def format_status(status):
    return status.text.replace(u'&amp;', u'&').replace('&lt;', '<').replace('&gt;', '>').replace('\n', ' ')


def parse(file_path):
    with open(file_path, 'r') as f:
        if file_path[-4:] == 'yaml':
            return yaml.load(f.read())

        elif file_path[-4:] == 'json':
            return json.load(f.read())


def fave_mentions():
    parser = argparse.ArgumentParser(description='fave mentions')
    parser.add_argument('-u', '--screen_name', type=str, help='User who will be doing the favoriting')
    parser.add_argument('-a', '--app', type=str, help='Name of the app to authenticate with')
    parser.add_argument('-c', '--api_config', type=str, help='(optional) file with api auth details')
    args = parser.parse_args()

    twitter = api.API(args.screen_name, args.api_config)
    twitter.fave_mentions()


def auto_follow():
    parser = argparse.ArgumentParser(description="automatic following")
    parser.add_argument('-u', '--screen_name', type=str, help='User who will be doing the favoriting')
    parser.add_argument('-a', '--app', type=str, help='Name of the app to authenticate with')
    parser.add_argument('-u', '--unfollow', action='store_true', help='Unfollow those who dont follow you')
    parser.add_argument('-c', '--api_config', type=str, help='(optional) file with api auth details')

    args = parser.parse_args()

    twitter = api.API(args.screen_name, args.api_config)

    if args.unfollow:
        twitter.unfollow()
    else:
        twitter.follow_back()

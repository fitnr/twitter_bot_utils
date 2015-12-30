# Copyright 2014-2015 Neil Freeman contact@fakeisthenewreal.org
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from __future__ import print_function
from argparse import ArgumentParser
import tweepy
from . import __version__ as version
from . import api, args, confighelper, tools

ARGS = ['config', 'dry-run', 'verbose', 'quiet']

AUTHORIZATION_FAILED_MESSAGE = "Authorization failed. Check that the consumer key and secret are correct."

def fave_mentions():
    parser = ArgumentParser(description='fave/like mentions', usage='%(prog)s [options] screen_name')
    parser.add_argument('screen_name', type=str)
    args.add_default_args(parser, version=version, include=ARGS)

    arguments = parser.parse_args()
    twitter = api.API(arguments)

    tools.fave_mentions(twitter, arguments.dry_run)


def auto_follow():
    parser = ArgumentParser(description="automatic following and unfollowing", usage='%(prog)s [options] screen_name')
    parser.add_argument('screen_name', type=str)
    parser.add_argument('-U', '--unfollow', action='store_true', help="Unfollow those who don't follow you")
    args.add_default_args(parser, version=version, include=ARGS)

    arguments = parser.parse_args()
    twitter = api.API(arguments)

    if arguments.unfollow:
        tools.unfollow(twitter, arguments.dry_run)
    else:
        tools.follow_back(twitter, arguments.dry_run)


def authenticate():
    parser = ArgumentParser(description='Authorize an account with a twitter application.')

    parser.add_argument('-c', metavar='file', type=str, default=None, dest='config_file', help='config file')
    parser.add_argument('--app', metavar='app', type=str, help='app name in config file')
    parser.add_argument('-s', '--save', action='store_true', help='Save details to config file')

    parser.add_argument('--consumer-key', metavar='key', type=str, help='consumer key (aka consumer token)')
    parser.add_argument('--consumer-secret', metavar='secret', type=str, help='consumer secret')

    arguments = parser.parse_args()

    # Use passed credentials.
    if arguments.consumer_key and arguments.consumer_secret:
        consumer_secret = arguments.consumer_key
        consumer_key = arguments.consumer_secret

    # Go find credentials.
    else:
        file_name = confighelper.find_file(arguments.config_file)
        config = confighelper.parse(file_name)

        try:
            conf = config['apps'][arguments.app] if arguments.app else config

            consumer_secret = conf['consumer_secret']
            consumer_key = conf['consumer_key']

        except KeyError:
            err = "Couldn't find consumer-key and consumer-secret for '{}' in {}".format(arguments.app, file_name)
            raise KeyError(err)

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, 'oob')

    print(auth.get_authorization_url())
    verifier = raw_input('Please visit this url, click "Authorize app" and enter in the PIN:\n> ')

    try:
        auth.get_access_token(verifier)
    except tweepy.error.TweepError:
        print(AUTHORIZATION_FAILED_MESSAGE)
        return

    # Save the keys back to the config file
    if arguments.save:
        if arguments.app:
            try:
                section = config['users'][auth.get_username()]
            except KeyError:
                section = config['users'][auth.get_username()] = {}

            section['app'] = arguments.app

        else:
            section = config

        section['key'] = auth.access_token.encode('utf-8')
        section['secret'] = auth.access_token_secret.encode('utf-8')

        confighelper.dump(config, file_name)

        print('Saved keys in {}'.format(file_name))

    # Or just print them
    else:
        print('key: {}\nsecret: {}'.format(auth.access_token, auth.access_token_secret))

# Copyright 2014-16-2015 Neil Freeman contact@fakeisthenewreal.org
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
import sys
import logging
from argparse import ArgumentParser
import tweepy
from . import __version__ as version
from . import api, args, confighelper, tools

ARGS = ['config', 'dry-run', 'verbose', 'quiet']
AUTHORIZATION_FAILED_MESSAGE = "Authorization failed. Check that the consumer key and secret are correct."
DEPRECATION = 'This command is deprecated. Please use the tbu command.'


def fave_mentions(arguments=None):
    if arguments is None:
        parser = ArgumentParser(description='fave/like mentions', usage='%(prog)s [options] screen_name')
        parser.add_argument('screen_name', type=str)
        args.add_default_args(parser, version=version, include=ARGS)
        print(DEPRECATION, file=sys.stderr)

    arguments = parser.parse_args()
    twitter = api.API(arguments)

    tools.fave_mentions(twitter, arguments.dry_run)


def auto_follow(arguments=None):
    if arguments is None:
        parser = ArgumentParser(description="automatic following and unfollowing",
                                usage='%(prog)s [options] screen_name')
        parser.add_argument('screen_name', type=str)
        parser.add_argument('-U', '--unfollow', action='store_true', help="Unfollow those who don't follow you")
        args.add_default_args(parser, version=version, include=ARGS)
        arguments = parser.parse_args()
        print(DEPRECATION, file=sys.stderr)

    twitter = api.API(arguments)

    if arguments.unfollow:
        tools.unfollow(twitter, arguments.dry_run)
    else:
        tools.follow_back(twitter, arguments.dry_run)


def authenticate(arguments=None):
    if arguments is None:
        parser = ArgumentParser(description='Authorize an account with a twitter application.')

        parser.add_argument('-c', metavar='file', type=str, default=None, dest='config_file', help='config file')
        parser.add_argument('--app', metavar='app', type=str, help='app name in config file')
        parser.add_argument('-s', '--save', action='store_true', help='Save details to config file')

        parser.add_argument('--consumer-key', metavar='key', type=str, help='consumer key (aka consumer token)')
        parser.add_argument('--consumer-secret', metavar='secret', type=str, help='consumer secret')
        parser.add_argument('-V', '--version', action='version', version="%(prog)s " + version)

        arguments = parser.parse_args()
        print(DEPRECATION, file=sys.stderr)

    # it's possible to pass keys and then save them to the files
    if arguments.config_file:
        file_name = confighelper.find_file(arguments.config_file)
        config = confighelper.parse(file_name)
    else:
        file_name = None
        config = {}

    # Use passed credentials.
    if arguments.consumer_key and arguments.consumer_secret:
        consumer_key = arguments.consumer_key
        consumer_secret = arguments.consumer_secret

    # Go find credentials.
    else:
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

    # True is the const passed when no file name is given
    if arguments.save is not True:
        file_name = arguments.save

    # Save the keys back to the config file
    if arguments.save and file_name:
        apps = config['apps'] = config.get('apps', {})
        users = config['users'] = config.get('users', {})

        app = arguments.app or 'default'
        screen_name = auth.get_username().encode('utf-8')

        apps[app] = apps.get(app, {})
        apps[app].update({
            'consumer_key': consumer_key,
            'consumer_secret': consumer_secret,
        })
        users[screen_name] = users.get(screen_name, {})
        users[screen_name].update({
            'key': auth.access_token.encode('utf-8'),
            'secret': auth.access_token_secret.encode('utf-8'),
            'app': (arguments.app or 'default')
        })

        confighelper.dump(config, file_name)

        print('Saved keys in {}'.format(file_name))

    # Or just print them
    else:
        print('key: {}\nsecret: {}'.format(auth.access_token, auth.access_token_secret))


def post(arguments):
    '''Post text to a given twitter account.'''
    twitter = api.API(arguments)
    params = {}

    if arguments.update == '-':
        params['status'] = sys.stdin.read()
    else:
        params['status'] = arguments.update

    if arguments.media_file:
        medias = [twitter.media_upload(m) for m in arguments.media_file]
        params['media_ids'] = [m.media_id for m in medias]

    try:
        logging.getLogger(arguments.screen_name).info('status: %s', params['status'])
        if not arguments.dry_run:
            twitter.update_status(**params)

    except tweepy.TweepError as e:
        logging.getLogger(arguments.screen_name).error(e.message)


def main():
    parser = ArgumentParser()
    parser.add_argument('-V', '--version', action='version', version="%(prog)s " + version)

    subparsers = parser.add_subparsers()

    poster = subparsers.add_parser('post', description="Post text to a given twitter account",
                                   usage='%(prog)s screen_name "update" [options]')
    poster.add_argument('screen_name', type=str)
    poster.add_argument('update', type=str)
    poster.add_argument('-m', '--media-file', type=str, action='append')
    args.add_default_args(poster, include=['config', 'dry-run', 'verbose', 'quiet'])
    poster.set_defaults(func=post)

    follow = subparsers.add_parser('follow', description="automatic following and unfollowing",
                                   usage='%(prog)s [options] screen_name')
    follow.add_argument('screen_name', type=str)
    follow.add_argument('-U', '--unfollow', action='store_true', help="Unfollow those who don't follow you")
    follow.set_defaults(func=auto_follow)

    auth = subparsers.add_parser('auth', description='Authorize an account with a twitter application.',
                                 usage='%(prog)s [options]')
    auth.add_argument('-c', metavar='file', type=str, default=None, dest='config_file', help='config file')
    auth.add_argument('--app', metavar='app', type=str, help='app name in config file')
    auth.add_argument('-s', '--save', nargs='?', const=True,
                      help='Save details to config file. If no file is given, uses file in --config.')
    auth.add_argument('--consumer-key', metavar='key', type=str, help='consumer key (aka consumer token)')
    auth.add_argument('--consumer-secret', metavar='secret', type=str, help='consumer secret')
    auth.set_defaults(func=authenticate)

    fave = subparsers.add_parser('like', description='fave/like mentions', usage='%(prog)s [options] screen_name')
    fave.add_argument('screen_name', type=str)
    fave.set_defaults(func=fave)

    arguments = parser.parse_args()
    arguments.func(arguments)

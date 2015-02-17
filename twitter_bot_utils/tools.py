#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# Copyright 2014 Neil Freeman
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

from . import api
from . import creation
from logging import getLogger

def follow_back(API):
    _autofollow(API, 'follow')


def unfollow(API):
    _autofollow(API, 'unfollow')


def _autofollow(API, action):
    logger = getLogger(API.screen_name)
    ignore = []

    # get the last 5000 followers
    try:
        followers = API.follower_ids()
        followers = [x.id_str for x in followers]

    except Exception as e:
        raise e

    # Get the last 5000 people user has followed
    try:
        friends = API.friend_ids()

    except Exception as e:
        raise e

    if action is "unfollow":
        method = API.destroy_friendship
        independent, dependent = followers, friends

    elif action is "follow":
        method = API.create_friendship
        independent, dependent = friends, followers

    logger.debug(u'{0}: found {1} friends, {2} followers'.format(action, len(friends), len(followers)))

    try:
        outgoing = API.friendships_outgoing()
        ignore = [x.id_str for x in outgoing]

    except Exception as e:
        raise e

    for uid in dependent:
        if uid in independent and uid not in ignore:
            try:
                method(id=uid)
                logger.debug('{0}: {1}'.format(action, uid))

            except Exception as e:
                raise e


def fave_mentions(API):
    logger = getLogger(API.screen_name)

    favs = API.favorites(include_entities=False, count=100)
    favs = [m.id_str for m in favs]
    faved = []

    try:
        mentions = API.mentions_timeline(trim_user=True, include_entities=False, count=75)
    except Exception as e:
        raise e

    for mention in mentions:
        # only try to fav if not in recent favs
        if mention.id_str not in favs:
            try:
                fav = API.create_favorite(mention.id_str, include_entities=False)
                faved.append(fav)
                logger.debug(u'faved {0}: {1}'.format(mention.id_str, mention.text))

            except Exception as e:
                raise e


def cli_fave_mentions():
    parser = creation.setup_args(description='fave mentions')
    parser.add_argument('screen_name', type=str, meta='[SCREEN NAME]', help='User who will be doing the favoriting')

    args = parser.parse_args()
    creation.defaults('fave_mentions', args)

    twitter = api.API(args.screen_name, args)
    fave_mentions(twitter)


def cli_auto_follow():
    parser = creation.setup_args(description="automatic following")
    parser.add_argument('-u', '--unfollow', action='store_true', help="Unfollow those who don't follow you")
    parser.add_argument('screen_name', type=str, meta='[SCREEN NAME]', help='User who will be doing the favoriting')

    args = parser.parse_args()
    creation.defaults('auto_follow', args)

    twitter = api.API(args.screen_name, args)

    if args.unfollow:
        unfollow(twitter)
    else:
        follow_back(twitter)

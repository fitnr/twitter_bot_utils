#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# Copyright 2014-16 Neil Freeman
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

from __future__ import unicode_literals
from time import sleep
from tweepy.error import RateLimitError, TweepError

RATE_LIMIT_RESET_MINUTES = 15

def follow_back(api, dry_run=None):
    _autofollow(api, 'follow', dry_run)


def unfollow(api, dry_run=None):
    _autofollow(api, 'unfollow', dry_run)


def _autofollow(api, action, dry_run):
    '''
    Follow back or unfollow the friends/followers of user authenicated in 'api'.
    :api twitter_bot_utils.api.API
    :dry_run bool don't actually (un)follow, just report
    '''
    try:
        # get the last 5000 followers
        followers = api.followers_ids()

        # Get the last 5000 people user has followed
        friends = api.friends_ids()

    except TweepError as e:
        api.logger.error('%s: error getting followers/followers', action)
        api.logger.error("%s", e)
        return

    if action == "unfollow":
        method = api.destroy_friendship
        independent, dependent = followers, friends

    elif action == "follow":
        method = api.create_friendship
        independent, dependent = friends, followers
    else:
        raise IndexError("Unknown action: {}".format(action))

    api.logger.info('%sing: found %s friends, %s followers', action, len(friends), len(followers))

    # auto-following:
    # for all my followers
    # if i don't already follow them: create friendship

    # auto-unfollowing:
    # for all my friends
    # if they don't follow me: destroy friendship
    targets = [x for x in dependent if x not in independent]

    for uid in targets:
        try:
            api.logger.info('%sing %s', action, uid)

            if not dry_run:
                method(id=uid)

        except RateLimitError:
            api.logger.warning("reached Twitter's rate limit, sleeping for %d minutes", RATE_LIMIT_RESET_MINUTES)
            sleep(RATE_LIMIT_RESET_MINUTES * 60)
            method(id=uid)

        except TweepError as e:
            api.logger.error('error %sing on %s', action, uid)
            api.logger.error("code %s: %s", e.api_code, e)


def fave_mentions(api, dry_run=None):
    '''
    Fave (aka like) recent mentions from user authenicated in 'api'.
    :api twitter_bot_utils.api.API
    :dry_run bool don't actually favorite, just report
    '''
    f = api.favorites(include_entities=False, count=150)
    favs = [m.id_str for m in f]

    try:
        mentions = api.mentions_timeline(trim_user=True, include_entities=False, count=75)
    except Exception as e:
        raise e

    for mention in mentions:
        # only try to fav if not in recent favs
        if mention.id_str not in favs:
            try:
                api.logger.info('liking %s: %s', mention.id_str, mention.text)

                if not dry_run:
                    api.create_favorite(mention.id_str, include_entities=False)

            except RateLimitError:
                api.logger.warning("reached Twitter's rate limit, sleeping for %d minutes", RATE_LIMIT_RESET_MINUTES)
                sleep(RATE_LIMIT_RESET_MINUTES * 60)
                api.create_favorite(mention.id_str, include_entities=False)

            except TweepError as e:
                api.logger.error('error liking %s', mention.id_str)
                api.logger.error("code %s: %s", e.api_code, e)

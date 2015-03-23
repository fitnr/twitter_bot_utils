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

from argparse import ArgumentParser
from . import __version__
from . import api
from . import args
from . import tools

def fave_mentions():
    parser = ArgumentParser(description='fave mentions', parents=[args.parent(__version__)])
    parser.add_argument('screen_name', type=str, metavar='[screen-name]', help='User who will be doing the favoriting')

    arguments = parser.parse_args()
    args.add_logger(arguments.screen_name, arguments.verbose)

    twitter = api.API(**vars(arguments))
    tools.fave_mentions(twitter, arguments.dry_run)


def auto_follow():
    parser = ArgumentParser(description="automatic following and unfollowing", parents=[args.parent(__version__)])
    parser.add_argument('-u', '--unfollow', action='store_true', help="Unfollow those who don't follow you")
    parser.add_argument('screen_name', type=str, metavar='[screen-name]', help='User who will be doing the (un)following')

    arguments = parser.parse_args()
    args.add_logger(arguments.screen_name, arguments.verbose)

    twitter = api.API(**vars(arguments))

    if arguments.unfollow:
        tools.unfollow(twitter, arguments.dry_run)
    else:
        tools.follow_back(twitter, arguments.dry_run)

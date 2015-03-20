from argparse import ArgumentParser
from . import __version__
from . import api
from . import args
from . import tools

def fave_mentions():
    parser = ArgumentParser(description='fave mentions', parents=[args.parent(__version__)])
    parser.add_argument('screen_name', type=str, metavar='[screen-name]', help='User who will be doing the favoriting')

    arguments = parser.parse_args()
    args.add_logger('fave_mentions', arguments.verbose)

    twitter = api.API(arguments.screen_name, arguments)
    tools.fave_mentions(twitter)


def auto_follow():
    parser = ArgumentParser(description="automatic following and unfollowing", parents=[args.parent(__version__)])
    parser.add_argument('-u', '--unfollow', action='store_true', help="Unfollow those who don't follow you")
    parser.add_argument('screen_name', type=str, metavar='[screen-name]', help='User who will be doing the (un)following')

    arguments = parser.parse_args()
    args.add_logger('auto_follow', arguments.verbose)

    twitter = api.API(arguments.screen_name, arguments)

    if arguments.unfollow:
        tools.unfollow(twitter)
    else:
        tools.follow_back(twitter)

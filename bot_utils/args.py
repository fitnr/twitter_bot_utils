import logging
import argparse
from . import levels

def add_default_args(parser):
    parser.add_argument('--api-config', metavar='PATH', default=None, type=str, help='path to config file to parse (json or yaml)')

    parser.add_argument('--key', type=str, help='Twitter user key')
    parser.add_argument('--secret', type=str, help='Twitter user secret')
    parser.add_argument('--consumer-key', type=str, help='Twitter application consumer key')
    parser.add_argument('--consumer-secret', type=str, help='Twitter application consumer secret')

    parser.add_argument('--since-id-file', type=str, help='path of JSON file with since IDs')

    parser.add_argument('--dry-run', action='store_true', help="Don't tweet, just output to stdout")
    parser.add_argument('-v', '--verbose', action='store_true', help="Log to stdout")


def defaults(screen_name, args):
    '''Interpret default args, set up API'''
    logger = logging.getLogger(screen_name)

    if args.api_config:
        logger.info('Using custom config file: {0}'.format(args.api_config))
    else:
        logger.info('Trying to use a default config')

    if args.verbose:
        levels.add_stdout_logger(screen_name)

def setup(botname, description):
    '''Set up an general argument parsing, logging'''
    levels.add_logger(botname)

    parser = argparse.ArgumentParser(description=description)
    add_default_args(parser)

    return parser

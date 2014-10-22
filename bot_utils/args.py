import logging
import argparse
from . import levels

def add_default_args(parser):
    parser.add_argument('-c', '--api_config', metavar='PATH', default=None, type=str, help='path to config file to parse (yaml)')
    parser.add_argument('--development', action='store_true', help="Don't tweet, just output to stdout")
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

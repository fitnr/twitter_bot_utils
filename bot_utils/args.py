import logging
import argparse
from . import config, levels

def add_default_args(parser):
    parser.add_argument('-c', '--api_config', metavar='PATH', default=None, type=str, help='path to config file to parse (yaml)')
    parser.add_argument('--development', action='store_true', help="Don't tweet, just output to stdout")

def parse_default_args(botname, args):
    logger = logging.getLogger(botname)

    if args.development:
        levels.add_stdout_logger(botname)

    if args.api_config:
        logger.info('Using custom config file: {0}'.format(args.api_config))
    else:
        logger.info('Trying to use a default config')

    config.load_config(args.api_config)

def setup(botname, description):
    '''Set up an general argument parsing, logging and api for bots'''
    levels.add_logger(botname)

    parser = argparse.ArgumentParser(description=description)
    add_default_args(parser)

    args = parser.parse_args()

    parse_default_args(botname, args)

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

import sys
import logging
import argparse


def add_default_args(parser, version=None, include=None):
    '''
    Add default arguments to a parser. These are:
        - config: argument for specifying a configuration file.
        - user: argument for specifying a user.
        - dry-run: option for running without side effects.
        - verbose: option for running verbosely.
        - quiet: option for running quietly.
        - version: option for spitting out version information.

    Args:
        version (str): version to return on <cli> --version
        include (Sequence): default arguments to add to cli. Default: (config, user, dry-run, verbose, quiet)
    '''
    include = include or ('config', 'user', 'dry-run', 'verbose', 'quiet')

    if 'config' in include:
        parser.add_argument('-c', '--config', dest='config_file', metavar='PATH', default=None,
                            type=str, help='bots config file (json or yaml)')
    if 'user' in include:
        parser.add_argument('-u', '--user', dest='screen_name', type=str, help="Twitter screen name")

    if 'dry-run' in include:
        parser.add_argument('-n', '--dry-run', action='store_true', help="Don't actually do anything")

    if 'verbose' in include:
        parser.add_argument('-v', '--verbose', action='store_true', help="Run talkatively")

    if 'quiet' in include:
        parser.add_argument('-q', '--quiet', action='store_true', help="Run quietly")

    if version:
        parser.add_argument('-V', '--version', action='version', version="%(prog)s " + version)


def parent(version=None, include=None):
    '''
    Return the default args as a parent parser, optionally adding a version

    Args:
        version (str): version to return on <cli> --version
        include (Sequence): default arguments to add to cli. Default: (config, user, dry-run, verbose, quiet)
    '''
    parser = argparse.ArgumentParser(add_help=False)
    add_default_args(parser, version=version, include=include)
    return parser


def add_logger(name, level=None, format=None):
    '''
    Set up a stdout logger.

    Args:
        name (str): name of the logger
        level: defaults to logging.INFO
        format (str): format string for logging output.
                      defaults to ``%(filename)-11s %(lineno)-3d: %(message)s``.

    Returns:
        The logger object.
    '''
    format = format or '%(filename)-11s %(lineno)-3d: %(message)s'
    log = logging.getLogger(name)

    # Set logging level.
    log.setLevel(level or logging.INFO)

    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(logging.Formatter(format))
    log.addHandler(ch)

    return log

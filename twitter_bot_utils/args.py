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

import logging
import argparse
from os import environ, path
from sys import stdout


def _add_boilerplate_args(parser, version=None):
    parser.add_argument('-c', '--config', metavar='PATH', default=None, type=str, help='path to config file to parse (json or yaml)')

    parser.add_argument('-n', '--dry-run', action='store_true', help="Don't actually run")
    parser.add_argument('-v', '--verbose', action='store_true', help="Log to stdout")

    if version:
        parser.add_argument('-V', '--version', action='version', version="%(prog)s " + version)

def add_default_args(parser, version=None):
    _add_boilerplate_args(parser, version)

    _add_user_args(parser)
    _add_consumer_args(parser)

def add_no_user_args(parser, version=None):
    _add_boilerplate_args(parser, version)
    _add_consumer_args(parser)

def _add_user_args(parser):
    parser.add_argument('--key', type=str, help='Twitter user key')
    parser.add_argument('--secret', type=str, help='Twitter user secret')

def _add_consumer_args(parser):
    parser.add_argument('--consumer-key', type=str, help='Twitter consumer key')
    parser.add_argument('--consumer-secret', type=str, help='Twitter consumer secret')

def parent(version=None):
    parser = argparse.ArgumentParser(add_help=False)
    add_default_args(parser, version=version)
    return parser


def add_logger(screen_name, verbose=None, **kwargs):
    '''Interpret default args, set up logger'''
    log = logger(screen_name, log_path=kwargs.get('logpath'))

    if verbose:
        stdout_logger(screen_name)

    return log


def _log_threshold():
    if environ.get('DEVELOPMENT', False) and not environ.get('production', False):
        # environment = 'development'
        threshold = logging.DEBUG
    else:
        # environment = 'production'
        threshold = logging.INFO

    return threshold


def logger(logger_name, log_path=None):
    log_path = log_path or path.join('~', 'bots', 'logs')
    log = logging.getLogger(logger_name)
    log.setLevel(_log_threshold())

    log_file = path.expanduser(path.join(log_path, logger_name + '.log'))
    fh = logging.FileHandler(log_file)
    fh.setFormatter(logging.Formatter('%(asctime)s %(name)-13s line %(lineno)d %(levelname)-5s %(message)s'))

    log.addHandler(fh)

    return log


def stdout_logger(logger_name):
    log = logging.getLogger(logger_name)

    ch = logging.StreamHandler(stdout)
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(logging.Formatter('%(filename)-10s %(lineno)-3d %(message)s'))

    log.addHandler(ch)

# -*- coding: utf-8 -*-
# Copyright 2014-17 Neil Freeman contact@fakeisthenewreal.org
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

"""Tools for managing bots.yaml and other config files."""

import json
from itertools import product
from os import getcwd, path

import tweepy
import yaml

CONFIG_DIRS = [
    getcwd(),
    "~",
    path.join("~", "bots"),
]

CONFIG_BASES = ["bots.yml", "bots.yaml", "bots.json"]


def configure(screen_name=None, config_file=None, app=None, **kwargs):
    """
    Set up a config dictionary using a bots.yaml config file and optional keyword args.

    Args:
        screen_name (str): screen_name of user to search for in config file
        config_file (str): Path to read for the config file
        app (str): Name of the app to look for in the config file. Defaults to the one set in users.{screen_name}.
        directories (str): Directories to read for the bots.yaml/json file. Defaults to ``CONFIG_DIRS``.
        bases (str): File names to look for in the directories. Defaults to ``CONFIG_BASES``.
    """
    # Use passed config file, or look for it in the default path.
    # Super-optionally, accept a different place to look for the file
    dirs = kwargs.pop("directories", None)
    bases = kwargs.pop("bases", None)
    file_config = {}
    if config_file is not False:
        config_file = find_file(config_file, dirs, bases)
        file_config = parse(config_file)

    # config and keys dicts
    # Pull non-authentication settings from the file.
    # Kwargs, user, app, and general settings are included, in that order of preference
    # Exclude apps and users sections from config
    config = {k: v for k, v in file_config.items() if k not in ("apps", "users")}

    user_conf = file_config.get("users", {}).get(screen_name, {})
    app = app or user_conf.get("app")
    app_conf = file_config.get("apps", {}).get(app, {})

    # Pull user and app data from the file
    config.update(app_conf)
    config.update(user_conf)

    # kwargs take precendence over config file
    config.update({k: v for k, v in kwargs.items() if v is not None})

    return config


def parse(file_path):
    """Parse a YAML file."""
    _, ext = path.splitext(file_path)

    if ext not in (".yaml", ".yml"):
        raise ValueError(f"Unrecognized config file type: {ext}")

    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def find_file(config_file=None, default_directories=None, default_bases=None):
    """Search for a config file in a list of files."""
    if config_file:
        if path.exists(path.expanduser(config_file)):
            return config_file

        raise FileNotFoundError(f"Config file not found: {config_file}")

    dirs = default_directories or CONFIG_DIRS
    dirs = [getcwd()] + dirs

    bases = default_bases or CONFIG_BASES

    for directory, base in product(dirs, bases):
        filepath = path.expanduser(path.join(directory, base))
        if path.exists(filepath):
            return filepath

    raise FileNotFoundError(f"Config file not found in {dirs}")


def setup_auth(**keys):
    """Set up Tweepy authentication using passed args or config file settings."""
    return tweepy.OAuth1UserHandler(
        consumer_key=keys["consumer_key"],
        consumer_secret=keys["consumer_secret"],
        access_token=keys.get("token", keys.get("key", keys.get("oauth_token"))),
        access_token_secret=keys.get("secret", keys.get("oauth_secret")),
    )


def dump(contents, file_path):
    """Dump a file's contents as a Python object"""
    _, ext = path.splitext(file_path)

    if ext not in (".yaml", ".yml"):
        raise ValueError(f"Unrecognized config file type {ext}")

    with open(file_path, "w", encoding="utf-8") as f:
        yaml.dump(contents, f, canonical=False, default_flow_style=False, indent=2)

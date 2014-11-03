from HTMLParser import HTMLParser
import yaml
import json


def has_url(status):
    return has_entity(status, 'urls')


def has_hashtag(status):
    return has_entity(status, 'hashtags')


def has_mention(status):
    return has_entity(status, 'user_mentions')


def has_media(status):
    return has_entity(status, 'media')


def has_symbol(status):
    return has_entity(status, 'symbols')


def has_entity(status, entitykey):
    try:
        return len(status.entities[entitykey]) > 0
    except (AttributeError, KeyError):
        return False


def has_entities(status):
    try:
        if len([i for v in status.entities.values() for i in v]) > 0:
            return True

    except (AttributeError, KeyError):
        pass

    return False


def format_status(status):
    return HTMLParser().unescape(status.text).replace('\n', ' ')


def config_parse(file_path):
    with open(file_path, 'r') as f:
        if file_path[-4:] == 'yaml':
            return yaml.load(f.read())

        elif file_path[-4:] == 'json':
            return json.load(f.read())

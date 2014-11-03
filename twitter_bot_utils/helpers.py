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


def remove_entity(status, entitytype):
    '''Use indices to remove given entity type from status text'''
    return remove_entities(status, [entitytype])

def remove_entities(status, entitylist):
    '''Remove entities for a list of items'''
    indices = [ent['indices'] for etype, entval in status.entities.items() for ent in entval if etype in entitylist]
    indices.sort(key=lambda x: x[0], reverse=True)

    text = status.text

    for start, end in indices:
        text = text[:start] + text[end:]
    return text

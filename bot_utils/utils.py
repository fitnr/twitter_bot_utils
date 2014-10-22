import yaml
import json

def no_entities(status):
    try:
        e = status.entities
    except AttributeError:
        return True
    if len(e['urls']) == 0 and len(e['hashtags']) == 0 and len(e['user_mentions']) == 0:
        return True
    else:
        return False

def clean_status(status):
    try:
        if no_entities(status) and status.metadata.get('iso_language_code') == 'en':
            return True
        else:
            return False
    except AttributeError:
        return False

def format_status(status):
    return status.text.replace(u'&amp;', u'&').replace('&lt;', '<').replace('&gt;', '>').replace('\n', ' ')


def parse(file_path):
    with open(file_path, 'r') as f:
        if file_path[-4:] == 'yaml':
            return yaml.load(f.read())

        elif file_path[-4:] == 'json':
            return json.load(f.read())

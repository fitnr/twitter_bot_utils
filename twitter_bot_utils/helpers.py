# -*- coding: utf-8 -*-
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
from __future__ import unicode_literals
from urllib import quote_plus
from HTMLParser import HTMLParser

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
        if len([i for v in list(status.entities.values()) for i in v]) > 0:
            return True

    except (AttributeError, KeyError):
        pass

    return False


def format_status(status):
    return format_text(status.text)


def format_text(text):
    return HTMLParser().unescape(text).replace('\n', ' ').strip()


def remove_entity(status, entitytype):
    '''Use indices to remove given entity type from status text'''
    return remove_entities(status, [entitytype])


def remove_entities(status, entitylist):
    '''Remove entities for a list of items'''
    try:
        entities = status.entities
        text = status.text
    except AttributeError:
        entities = status.get('entities', dict())
        text = status['text']

    indices = [ent['indices'] for etype, entval in list(entities.items()) for ent in entval if etype in entitylist]
    indices.sort(key=lambda x: x[0], reverse=True)

    for start, end in indices:
        text = text[:start] + text[end:]
    return text


def replace_urls(status):
    '''replace URLS with expanded urls'''
    text = status.text

    if not has_url(status):
        return text

    urls = [(e['indices'], e['expanded_url']) for e in status.entities['urls']]
    urls.sort(key=lambda x: x[0][0], reverse=True)

    for (start, end), url in urls:
        text = text[:start] + url + text[end:]

    return text


def shorten(string, length=140, ellipsis=None):
    '''Shorten a string to 140 characters without breaking words.
    Optionally add an ellipsis character: '…' if ellipsis=True, or a given string
    e.g. ellipsis=' (cut)' '''
    string = string.strip()

    if len(string) > length:
        if ellipsis is True:
            ellipsis = '…'
        else:
            ellipsis = ellipsis or ''

        L = length - len(ellipsis)

        return ' '.join(string[:L].split(' ')[:-1]).strip(',;:') + ellipsis

    else:
        return string


def queryize(terms, exclude_screen_name=None):
    '''Create query from list of terms, using OR
    but intelligently excluding terms beginning with '-' (Twitter's NOT operator).
    Optionally add -from:exclude_screen_name.
    Returns a string ready to be passed to tweepy.API.search
    '''
    ors = (x for x in terms if x[0] != '-')
    nots = (x for x in terms if x[0] == '-')
    sn = " -from:" + exclude_screen_name + ' ' if exclude_screen_name else ' '
    return quote_plus(' OR '.join(ors) + sn + ' '.join(nots))

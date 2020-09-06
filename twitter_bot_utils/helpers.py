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
from __future__ import unicode_literals
import re
import unicodedata
try:
    import HTMLParser
    parser = HTMLParser.HTMLParser()
except ImportError:
    from html import parser


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

    except AttributeError:
        return len(status['entities'][entitykey]) > 0


def has_entities(status):
    """
    Returns true if a Status object has entities.

    Args:
        status: either a tweepy.Status object or a dict returned from Twitter API
    """
    try:
        if sum(len(v) for v in status.entities.values()) > 0:
            return True

    except AttributeError:
        if sum(len(v) for v in status['entities'].values()) > 0:
            return True

    return False

def format_status(status):
    return format_text(status.text)

def format_text(text):
    return parser.unescape(text).strip()

def remove_mentions(status):
    '''Remove mentions from status text'''
    return remove_entities(status, ['user_mentions'])

def remove_urls(status):
    '''Remove urls from status text'''
    return remove_entities(status, ['urls'])

def remove_symbols(status):
    '''Remove symbols from status text'''
    return remove_entities(status, ['symbols'])

def remove_hashtags(status):
    '''Remove hashtags from status text'''
    return remove_entities(status, ['hastags'])

def remove_entity(status, entitytype):
    '''Use indices to remove given entity type from status text'''
    return remove_entities(status, [entitytype])


def remove_entities(status, entitylist):
    '''Remove entities for a list of items.'''
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
    '''
    Replace shorturls in a status with expanded urls.

    Args:
        status (tweepy.status): A tweepy status object

    Returns:
        str
    '''
    text = status.text

    if not has_url(status):
        return text

    urls = [(e['indices'], e['expanded_url']) for e in status.entities['urls']]
    urls.sort(key=lambda x: x[0][0], reverse=True)

    for (start, end), url in urls:
        text = text[:start] + url + text[end:]

    return text


def shorten(string, length=140, ellipsis=None):
    '''
    Shorten a string to 140 characters without breaking words.
    Optionally add an ellipsis character: '…' if ellipsis=True, or a given string
    e.g. ellipsis=' (cut)'
    '''
    string = string.strip()

    if len(string) > length:
        if ellipsis is True:
            ellipsis = '…'
        else:
            ellipsis = ellipsis or ''

        L = length - len(ellipsis)

        return ' '.join(string[:L].split(' ')[:-1]).strip(',;:.') + ellipsis

    else:
        return string


def queryize(terms, exclude_screen_name=None):
    '''
    Create query from list of terms, using OR
    but intelligently excluding terms beginning with '-' (Twitter's NOT operator).
    Optionally add -from:exclude_screen_name.

    >>> helpers.queryize(['apple', 'orange', '-peach'])
    u'apple OR orange -peach'

    Args:
        terms (list): Search terms.
        exclude_screen_name (str): A single screen name to exclude from the search.

    Returns:
        A string ready to be passed to tweepy.API.search
    '''
    ors = ' OR '.join('"{}"'.format(x) for x in terms if not x.startswith('-'))
    nots = ' '.join('-"{}"'.format(x[1:]) for x in terms if x.startswith('-'))
    sn = "-from:{}".format(exclude_screen_name) if exclude_screen_name else ''
    return ' '.join((ors, nots, sn))


def chomp(text, max_len=280, split=None):
    '''
    Shorten a string so that it fits under max_len, splitting it at 'split'.
    Not guaranteed to return a string under max_len, as it may not be possible

    Args:
        text (str): String to shorten
        max_len (int): maximum length. default 140
        split (str): strings to split on (default is common punctuation: "-;,.")
    '''
    split = split or '—;,.'
    while length(text) > max_len:
        try:
            text = re.split(r'[' + split + ']', text[::-1], 1)[1][::-1]
        except IndexError:
            return text

    return text


def length(text, maxval=None, *args):
    '''
    Count the length of a str the way Twitter does,
    double-counting "wide" characters (e.g. ideographs, emoji)

    Args:
        text (str): Text to count.
        maxval (int): The maximum encoding that will be counted as 1 character.
            Defaults to 4351 (ჿ GEORGIAN LETTER LABIAL SIGN, U+10FF)

    Returns:
        int
    '''
    maxval = maxval or 4351
    try:
        assert isinstance(text, str)
    except AssertionError:
        raise TypeError('helpers.length requires a string argument')
    return sum(2 if ord(x) > maxval else 1 for x in unicodedata.normalize('NFC', text))

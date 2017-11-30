# -*- coding: utf-8 -*-
# Copyright 2014-2017 Neil Freeman
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
import os
import mimetypes
from time import sleep
import logging
from argparse import Namespace

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

import tweepy
from tweepy.error import TweepError
from tweepy.binder import bind_api
from tweepy.parsers import RawParser
from .confighelper import configure
from . import args as tbu_args

PROTECTED_INFO = [
    'consumer_key',
    'consumer_secret',
    'key',
    'token',
    'oauth_token',
    'secret',
    'oauth_secret',
]

IMAGE_MIMETYPES = ('image/gif', 'image/jpeg', 'image/png', 'image/webp')

CHUNKED_MIMETYPES = ('image/gif', 'image/jpeg', 'image/png', 'image/webp', 'video/mp4')

def getfilesize(filename, f=None):
    if f is None:
        try:
            size = os.path.getsize(filename)
        except os.error as e:
            raise TweepError('Unable to access file: %s' % e.strerror)

    else:
        f.seek(0, 2)  # Seek to end of file
        size = f.tell()
        f.seek(0)  # Reset to beginning of file

    return size

class API(tweepy.API):

    '''
    Extends the tweepy API with config-file handling.

    Args:
        args (Namespace): argparse.Namespace to read.
        screen_name (str): Twitter screen name
        config_file (str): Config file. When False, don't read any config files. Defaults to bots.json or bots.yaml in ~/ or ~/bots/.
        logger_name (str): Use a logger with this name. Defaults to screen_name
        format (str): Format for logger. Defaults to 'file lineno: message'
        verbose (bool): Set logging level to DEBUG
        quiet (bool): Set logging level to ERROR. Overrides verbose.
        use_env (bool): Allow environment variables to override settings. Default: True
        kwargs: Other settings will be passed to the config
    '''

    _last_tweet = _last_reply = _last_retweet = None

    max_size_standard = 5120  # standard uploads must be less then 5 MB
    max_size_chunked = 15360  # chunked uploads must be less than 15 MB

    def __init__(self, args=None, **kwargs):
        '''
        Construct the tbu.API object.
        '''

        # Update the kwargs with non-None contents of args
        if isinstance(args, Namespace):
            kwargs.update({k: v for k, v in vars(args).items() if v is not None})

        self._screen_name = kwargs.pop('screen_name', None)

        # Add a logger
        level = logging.DEBUG if kwargs.pop('verbose', None) else None
        level = logging.ERROR if kwargs.get('quiet', None) else level
        self.logger = tbu_args.add_logger(kwargs.pop('logger_name', self._screen_name), level,
                                          kwargs.pop('format', None))

        # get config file and parse it
        config = configure(self._screen_name, **kwargs)
        self._config = {k: v for k, v in config.items() if k not in PROTECTED_INFO}
        keys = {k: v for k, v in config.items() if k in PROTECTED_INFO}
        if kwargs.get('use_env', True):
            keys.update({
                k: os.environ['TWITTER_' + k.upper()] for k in PROTECTED_INFO
                if k not in keys and 'TWITTER_' + k.upper() in os.environ
            })

        try:
            # setup auth
            auth = tweepy.OAuthHandler(consumer_key=keys['consumer_key'], consumer_secret=keys['consumer_secret'])

            try:
                auth.set_access_token(
                    key=keys.get('token', keys.get('key', keys.get('oauth_token'))),
                    secret=keys.get('secret', keys.get('oauth_secret'))
                )

            except KeyError:
                # API won't have an access key
                pass

        except KeyError:
            missing = [p for p in PROTECTED_INFO if p not in keys]
            raise ValueError("Incomplete config. Missing {}".format(missing))

        # initiate api connection
        super(API, self).__init__(auth)

    @property
    def config(self):
        return self._config

    @property
    def screen_name(self):
        return self._screen_name

    @property
    def app(self):
        return self._config['app']

    def _sinces(self):
        tl = self.user_timeline(self.screen_name, count=1000, include_rts=True, exclude_replies=False)

        if len(tl) > 0:
            self._last_tweet = tl[0].id
        else:
            self._last_tweet = self._last_reply = self._last_retweet = None
            return

        try:
            self._last_reply = max(t.id for t in tl if t.in_reply_to_user_id)
        except ValueError:
            self._last_reply = None

        try:
            self._last_retweet = max(t.id for t in tl if t.retweeted)
        except ValueError:
            self._last_retweet = None

    def _last(self, last_what, refresh):
        if refresh or getattr(self, last_what) is None:
            self._sinces()

        return getattr(self, last_what)

    @property
    def last_tweet(self, refresh=None):
        return self._last('_last_tweet', refresh)

    @property
    def last_reply(self, refresh=None):
        return self._last('_last_reply', refresh)

    @property
    def last_retweet(self, refresh=None):
        return self._last('_last_retweet', refresh)

    def update_status(self, *pargs, **kwargs):
        """
        Wrapper for tweepy.api.update_status with a 10s wait when twitter is over capacity
        """
        try:
            return super(API, self).update_status(*pargs, **kwargs)

        except tweepy.TweepError as e:
            if getattr(e, 'api_code', None) == 503:
                sleep(10)
                return super(API, self).update_status(*pargs, **kwargs)
            else:
                raise e


    def media_upload(self, filename, *args, **kwargs):
        """ :reference: https://dev.twitter.com/rest/reference/post/media/upload
            :reference https://dev.twitter.com/rest/reference/post/media/upload-chunked
            :allowed_param:
        """
        f = kwargs.pop('file', None)

        mime, _ = mimetypes.guess_type(filename)
        size = getfilesize(filename, f)

        if mime in IMAGE_MIMETYPES and size < self.max_size_standard:
            return self.image_upload(filename, file=f, *args, **kwargs)

        elif mime in CHUNKED_MIMETYPES:
            return self.upload_chunked(filename, file=f, *args, **kwargs)

        else:
            raise TweepError("Can't upload media with mime type %s" % mime)

    def image_upload(self, filename, *args, **kwargs):
        """ :reference: https://dev.twitter.com/rest/reference/post/media/upload
            :allowed_param:
        """
        f = kwargs.pop('file', None)
        headers, post_data = API._pack_image(filename, self.max_size_standard, form_field='media', f=f)
        kwargs.update({'headers': headers, 'post_data': post_data})

        return bind_api(
            api=self,
            path='/media/upload.json',
            method='POST',
            payload_type='media',
            allowed_param=[],
            require_auth=True,
            upload_api=True
        )(*args, **kwargs)

    def upload_chunked(self, filename, *args, **kwargs):
        """ :reference https://dev.twitter.com/rest/reference/post/media/upload-chunked
            :allowed_param:
        """
        f = kwargs.pop('file', None)

        # Media category is dependant on whether media is attached to a tweet
        # or to a direct message. Assume tweet by default.
        is_direct_message = kwargs.pop('is_direct_message', False)

        # Initialize upload (Twitter cannot handle videos > 15 MB)
        headers, post_data, fp = API._chunk_media('init', filename, self.max_size_chunked, form_field='media', f=f, is_direct_message=is_direct_message)
        kwargs.update({'headers': headers, 'post_data': post_data})

        # Send the INIT request
        media_info = bind_api(
            api=self,
            path='/media/upload.json',
            method='POST',
            payload_type='media',
            allowed_param=[],
            require_auth=True,
            upload_api=True
        )(*args, **kwargs)

        # If a media ID has been generated, we can send the file
        if media_info.media_id:
            # default chunk size is 1MB, can be overridden with keyword argument.
            # minimum chunk size is 16K, which keeps the maximum number of chunks under 999
            chunk_size = kwargs.pop('chunk_size', 1024 * 1024)
            chunk_size = max(chunk_size, 16 * 2014)

            fsize = getfilesize(filename, f)
            nloops = int(fsize / chunk_size) + (1 if fsize % chunk_size > 0 else 0)
            for i in range(nloops):
                headers, post_data, fp = API._chunk_media('append', filename, self.max_size_chunked, chunk_size=chunk_size, f=fp, media_id=media_info.media_id, segment_index=i, is_direct_message=is_direct_message)
                kwargs.update({ 'headers': headers, 'post_data': post_data, 'parser': RawParser() })
                # The APPEND command returns an empty response body
                bind_api(
                    api=self,
                    path='/media/upload.json',
                    method='POST',
                    payload_type='media',
                    allowed_param=[],
                    require_auth=True,
                    upload_api=True
                )(*args, **kwargs)
            # When all chunks have been sent, we can finalize.
            headers, post_data, fp = API._chunk_media('finalize', filename, self.max_size_chunked, media_id=media_info.media_id, is_direct_message=is_direct_message)
            kwargs = {'headers': headers, 'post_data': post_data}

            # The FINALIZE command returns media information
            return bind_api(
                api=self,
                path='/media/upload.json',
                method='POST',
                payload_type='media',
                allowed_param=[],
                require_auth=True,
                upload_api=True
            )(*args, **kwargs)
        else:
            return media_info

    @staticmethod
    def _chunk_media(command, filename, max_size, form_field="media", chunk_size=4096, f=None, media_id=None, segment_index=0, is_direct_message=False):
        fp = None
        if command == 'init':
            file_size = getfilesize(filename, f)
            if file_size > (max_size * 1024):
                raise TweepError('File is too big, must be less than %skb.' % max_size)

            if f is None:
                # build the multipart-formdata body
                fp = open(filename, 'rb')
            else:
                fp = f
        elif command != 'finalize':
            if f is not None:
                fp = f
            else:
                raise TweepError('File input for APPEND is mandatory.')

        # video must be mp4
        file_type, _ = mimetypes.guess_type(filename)

        if file_type is None:
            raise TweepError('Could not determine file type')

        if file_type not in CHUNKED_MIMETYPES:
            raise TweepError('Invalid file type for video: %s' % file_type)

        BOUNDARY = b'Tw3ePy'
        body = list()
        if command == 'init':
            query = {
                'command': 'INIT',
                'media_type': file_type,
                'total_bytes': file_size,
                'media_category': API._get_media_category(
                    is_direct_message, file_type)
            }
            body.append(urlencode(query).encode('utf-8'))
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'
            }
        elif command == 'append':
            if media_id is None:
                raise TweepError('Media ID is required for APPEND command.')
            body.append(b'--' + BOUNDARY)
            body.append('Content-Disposition: form-data; name="command"'.encode('utf-8'))
            body.append(b'')
            body.append(b'APPEND')
            body.append(b'--' + BOUNDARY)
            body.append('Content-Disposition: form-data; name="media_id"'.encode('utf-8'))
            body.append(b'')
            body.append(str(media_id).encode('utf-8'))
            body.append(b'--' + BOUNDARY)
            body.append('Content-Disposition: form-data; name="segment_index"'.encode('utf-8'))
            body.append(b'')
            body.append(str(segment_index).encode('utf-8'))
            body.append(b'--' + BOUNDARY)
            body.append('Content-Disposition: form-data; name="{0}"; filename="{1}"'.format(form_field, os.path.basename(filename)).encode('utf-8'))
            body.append('Content-Type: {0}'.format(file_type).encode('utf-8'))
            body.append(b'')
            body.append(fp.read(chunk_size))
            body.append(b'--' + BOUNDARY + b'--')
            headers = {
                'Content-Type': 'multipart/form-data; boundary=Tw3ePy'
            }
        elif command == 'finalize':
            if media_id is None:
                raise TweepError('Media ID is required for FINALIZE command.')
            body.append(
                urlencode({
                    'command': 'FINALIZE',
                    'media_id': media_id
                }).encode('utf-8')
            )
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'
            }

        body = b'\r\n'.join(body)
        # build headers
        headers['Content-Length'] = str(len(body))

        return headers, body, fp

    @staticmethod
    def _get_media_category(is_direct_message, file_type):
        """ :reference: https://developer.twitter.com/en/docs/direct-messages/message-attachments/guides/attaching-media
            :allowed_param:
        """
        if is_direct_message:
            prefix = 'dm'
        else:
            prefix = 'tweet'

        if file_type in IMAGE_MIMETYPES:
            if file_type == 'image/gif':
                return prefix + '_gif'
            else:
                return prefix + '_image'
        elif file_type == 'video/mp4':
            return prefix + '_video'

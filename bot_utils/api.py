import tweepy
from os import path
from . import helpers

CONFIG_PATHS = [
    'botrc',
    'bots.yaml',
    'bots.json',
    'bots/botrc',
    'bots/bots.yaml',
    'bots/bots.json'
]

class API(tweepy.API):

    '''Extends the tweepy API with config-file handling'''

    app_name = None
    screen_name = None

    _last_tweet, _last_reply, _last_retweet = None, None, None

    def __init__(self, screen_name, **kwargs):
        if kwargs.get('config') and path.exists(kwargs['config']):
            file_name = kwargs['config']

        else:
            for pth in CONFIG_PATHS:
                expanded_path = path.join(path.expanduser('~'), pth)

                if path.exists(expanded_path):
                    file_name = expanded_path
                    break

        try:
            self._config = helpers.config_parse(file_name)

        except (AttributeError, IOError):
            if kwargs.get('config'):
                msg = 'Custom config file not found: {0}'.format(kwargs['config'])

            else:
                msg = 'Config file not found in ~/bots.{json,yaml} or ~/bots/bots.{json,yaml} or ~/botrc or ~/bots/botrc'

            raise IOError(msg)

        if 'users' not in self._config or 'apps' not in self._config:
            raise AttributeError('Config file incomplete. Must contain both an apps and a users section')

        self.screen_name = screen_name
        self.app_name = self.user['app']

        auth = self._setup_auth(kwargs)

        super(API, self).__init__(auth)

    def _setup_auth(self, kwargs):
        '''Setup tweepy authentication using passed args or config file settings'''

        consumer_key = kwargs.get('consumer_key') or self.app['consumer_key']
        consumer_secret = kwargs.get('consumer_secret') or self.app['consumer_secret']

        key = kwargs.get('key') or self.user['key']
        secret = kwargs.get('secret') or self.user['secret']

        auth = tweepy.OAuthHandler(consumer_key=consumer_key, consumer_secret=consumer_secret)
        auth.set_access_token(key=key, secret=secret)

        return auth

    def _get(self, section, key):
        if key not in self._config[section]:
            raise IndexError('Key not found in {section} section of config: {key}'.format(section=section, key=key))

        return self._config[section][key]

    @property
    def user(self):
        return self._get('users', self.screen_name)

    @property
    def app(self):
        return self._get('apps', self.app_name)

    @property
    def last_tweet(self):
        if not self._last_tweet:
            self._last_tweet = self.user_timeline().pop(0).id

        return self._last_tweet

    @property
    def last_reply(self):
        if not self._last_reply:
            tl = self.user_timeline()
            filtered = [tweet for tweet in tl if tweet.in_reply_to_user_id]
            self._last_reply = filtered[0].id

        return self._last_reply

    @property
    def last_retweet(self):
        if not self._last_retweet:
            tl = self.user_timeline()
            filtered = [tweet for tweet in tl if tweet.retweeted]
            self._last_retweet = filtered[0].id

        return self._last_retweet

    def fave_mentions(self):
        favs = self.favorites(include_entities=False, count=100)
        favs = [m.id_str for m in favs]
        faved = []

        try:
            mentions = self.mentions_timeline(trim_user=True, include_entities=False, count=75)
        except Exception, e:
            raise e

        for mention in mentions:
            # only try to fav if not in recent favs
            if mention.id_str not in favs:
                try:
                    fav = self.create_favorite(mention.id_str, include_entities=False)
                    faved.append(fav)

                except Exception, e:
                    raise e

    def follow_back(self):
        self._autofollow('follow')

    def unfollow(self):
        self._autofollow('unfollow')

    def _autofollow(self, action):
        ignore = []

        # get the last 5000 followers
        try:
            followers = self.follower_ids()
            followers = [x.id_str for x in followers]

        except Exception, e:
            raise e

        # Get the last 5000 people user has followed
        try:
            friends = self.friend_ids()

        except Exception, e:
            raise e

        if action is "unfollow":
            method = self.destroy_friendship
            independent, dependent = followers, friends

        elif action is "follow":
            method = self.create_friendship
            independent, dependent = friends, followers

        try:
            outgoing = self.friendships_outgoing()
            ignore = [x.id_str for x in outgoing]

        except Exception, e:
            raise e

        for uid in dependent:
            if uid in independent and uid not in ignore:
                try:
                    method(id=uid)

                except Exception, e:
                    raise e

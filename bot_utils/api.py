import tweepy
from os import path
import json
from . import helpers


class API(tweepy.API):

    '''Extends the tweepy API with config-file handling'''

    app_name = None
    screen_name = None

    possible_paths = [
        'bots.yaml',
        'bots.json',
        'bots/bots.yaml',
        'bots/bots.json'
    ]

    _since_ids = None

    def __init__(self, screen_name, args):
        if args.api_config and path.exists(args.api_config):
            file_name = args.api_config

        else:
            for pth in self.possible_paths:
                expanded_path = path.join(path.expanduser('~'), pth)

                if path.exists(expanded_path):
                    file_name = expanded_path
                    break

        try:
            self._config = helpers.parse(file_name)

        except (AttributeError, IOError):
            if args.api_config:
                msg = 'Custom config file not found: {0}'.format(args.api_config)

            else:
                msg = 'Config file not found in ~/bots.{json,yaml} or ~/bots/bots.{json,yaml}'

            raise IOError(msg)

        if 'users' not in self._config or 'apps' not in self._config:
            raise AttributeError('Config file incomplete. Must contain both an apps and a users section')

        self.screen_name = screen_name

        if args.consumer_key and args.consumer_secret:
            auth = tweepy.OAuthHandler(consumer_key=args.consumer_key, consumer_secret=args.consumer_secret)
        else:
            self.app_name = self.user['app']
            auth = tweepy.OAuthHandler(**self.app)

        if args.key and args.secret:
            auth.set_access_token(key=args.key, secret=args.secret)
        else:
            auth.set_access_token(key=self.user['key'], secret=self.user['secret'])

        super(API, self).__init__(auth)

        self._formatted_since_id = path.expanduser(self._config['since_id_file'].format(data_path=self._config['data_path']))

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
    def since_id(self):
        if not self._since_ids:
            self._since_ids = self._since_id_contents()
        return self._since_ids.get(self.screen_name, None)

    @since_id.setter
    def since_id(self, value):
        self._since_ids[self.screen_name] = value

    def save_since_id(self, _id):
        self._since_ids[self.screen_name] = _id

        with open(self._formatted_since_id, 'w+') as f:
            json.dump(self._since_ids, f)

    def _since_id_contents(self):
        try:
            with open(self._formatted_since_id, 'rb') as f:
                return json.load(f)
        except IOError:
            return dict()

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

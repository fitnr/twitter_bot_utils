## twitter bot utils

These Python utilities make it a little easier to set up a Twitter bot, with an eye to making command-line options easy to reproduce.

The utilities are a wrapper for the excellent [Tweepy](http://tweepy.org) and [argparse]() libraries, which handle the Twitter API and command line options, respectively. They're ideal if you want to store the configuration settings for a few bots in a config file.

### Setting up a tweepy API

Easily set up the api with a yaml or json config file:

````python
from twitter_bot_utils import api

# Different ways to create the tweepy API object.
twitter = api.API('MyBotName', args)
twitter = api.API('MyBotName', config='path/to/config.yaml')
twitter = api.API('MyBotName', consumer_key='...', consumer_secret='...', key='...', secret='...')

# If the config file is called bots.yaml or bots.json or botrc, and lives at ~/ or ~/bots,
# twitter bot utils will find it automatically
twitter = api.API('MyBotName')
````

Example config file layout:

````yaml
users:
    # twitter screen_name
    MyBotName:
        key: $oauth_key
        secret: $oauth_key_secret
        # The app key should match a key in apps below
        app: my_app_name
        custom_setting: 'hello world'

    other_bot:
        key: ...
        secret: ...
        app: my_app_name

apps:
    my_app_name:
        consumer_key: ...
        consumer_secret: ...

foo: bar

````

The config file, minus the 'users' and 'apps' section, is available to you, so use it for more settings and options. If this YAML file is the settings file for the code above:

````python
twitter.config['foo']
# returns 'bar'

# The current user and app are also available:
twitter.user['custom_setting']
# hello world
````

### Recent tweets

It's often useful to know what a bot has done recently. There are three properties in the twitter_bot_utils.API object for this. Use them for setting up since_id arguments.

````python
twitter = api.API('MyBotName')

twitter.last_tweet
# id of most recent tweet from MyBotName

twitter.last_reply
# id of most recent reply from MyBotName

twitter.last_retweet
# id of most recent retweet from MyBotName

# What's happened since the last time the bot was active?
twitter.search('#botALLY', since_id=twitter.last_tweet)
````

### Default Command Line Options

Some usefulcommand line flags are available by default:

* -n, --dry-run: Don't tweet, just output to stdout
* -v, --verbose: Log to stdout
* -c PATH, --config PATH: path to a config file. This is a JSON or YAML file laid out according to the below format. 

You can also pass authentication arguments with these options arguments.

* --key KEY: Twitter user key
* --secret SECRET: Twitter user secret
* --consumer-key CONSUMER_KEY: Twitter application consumer key
* --consumer-secret CONSUMER_SECRET: Twitter application consumer secret

````python
import logging
import twitter_bot_utils

# This sets up an argparse.ArgumentParser with some default arguments, which are explained below
parser = twitter_bot_utils.setup_args('MyBotName', description='Tweet something')

parser.add_argument('-m', '--my-arg', help="You're passing an argument to argparse.ArgumentParser")

args = parser.parse_args()

# Parse the default args. If vocal is set, the logger will output to stdout.
twitter_bot_utils.defaults('MyBotName', args)

# That's right, utils set up a logger for you. It has the same name as your bot
logger = logging.getLogger('MyBotName')

# Do logic here to generate a tweet somehow
tweet = my_tweet_function()

# Use args.dry_run to control tweeting
if not args.dry_run:
    twitter.update_status(tweet)
````

### Helpers

## Checking for entities

Easily check if tweets have specific entities:

````python
import twitter_bot_utils

# Don't set include_entities to False and expect the below to work
statuses = twitter.search('example search', include_entities=True)

status = status[0]

twitter_bot_utils.helpers.has_mention(status)
# returns True if status has one or more mentions, otherwise False 

twitter_bot_utils.helpers.has_hashtag(status)
# returns True if status has one or more hashtags, otherwise False 

twitter_bot_utils.helpers.has_media(status)
# returns True if status has one or more media entities (images, video), otherwise False 

twitter_bot_utils.helpers.has_entities(status)
# returns True if status has any entities

# These also exist:
# twitter_bot_utils.helpers.has_url
# twitter_bot_utils.helpers.has_symbol
````

## Filtering out entities

Easily remove entities from a tweet's text.

````python
import twitter_bot_utils

api = twitter_bot_utils.api.API('MyBotName')

results = api.search("special topic")

results[0].text
# 'This is an example tweet with a #hashtag and a link http://foo.com'

twitter_bot_utils.helpers.remove_entity(results[0], 'hashtags')
# 'This is an example tweet with a  and a link http://foo.com'

twitter_bot_utils.helpers.remove_entity(results[0], 'urls')
# 'This is an example tweet with a #hashtag and a link '

# Remove multiple entities with remove_entities.
twitter_bot_utils.helpers.remove_entities(results[0], ['urls', 'hashtags', 'media'])
# 'This is an example tweet with a  and a link '
````

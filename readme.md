# twitter bot utils

Twitter bot utils make it a little easier to set up a Twitter bot, with an eye to making config and command-line options easy to manage and reproduce. They're intended for managing a small-to-medium-sized coterie of Twitter accounts on one machine. The package is a super-simple wrapper for the excellent [Tweepy](http://tweepy.org) library. It also provides shortcuts for setting up command line tools with [argparse](https://docs.python.org/3/library/argparse.html).

This package is intended to assist with the creation of bots for artistic or personal projects. Don't use it to spam or harrass people.

Works with Python 2.7 and 3.4 (2.6 & 3.3 probably work, too).

Install with `pip install twitter_bot_utils`.

## Setting up a tweepy API

The main goal of Twitter bot utils is to create Tweepy instances with authentication data stored in a simple conf file. This gives botmakers a simple, reusable place to store keys outside of source control.

By default, twitter_bot_utils will read settings from a YAML or JSON config file. By default, it looks in the ~/ and ~/bots directories for files named "bots.yaml", "bots.json", or "botrc". Custom config files can be set, too, of course.

````python
from twitter_bot_utils import api

# Automatically check for a config file in the above-named directories
twitter = api.API('MyBotName')

# Specify a specific config file
twitter = api.API('MyBotName', config='path/to/config.yaml')

# This is possible, although you should consider just using Tweepy directly
twitter = api.API('MyBotName', consumer_key='...', consumer_secret='...', key='...', secret='...')
````

Twitter bot utils comes with some built-in command line parsers, and the API object will also happily consume the result of `argparse.parser.parse_args()` (see below for details).

### Config file setup

Custom settings in the config are available at runtime, so use the config file for any special settings you want.

Example config file layout (This is YAML, JSON works, too):

````yaml
# ~/bots.yaml

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

Using the config settings:

````python
import twitter_bot_utils

# Look for config in the default places mentioned above:
twitter = twitter_bot_utils.api.API('MyBotName')

twitter.config['foo']
# returns 'bar'

# The current user and app are also available:
twitter.user['custom_setting']
# hello world
````

Setting a custom config file is simple:

````python
# The config keyword argument will set a custom file location
twitter = twitter_bot_utils.api.API('MyBotName', config='special/file/path.yaml')
````

### Without user authentication

Some Twitter API queries don't require user authentication. To set up an Tweepy API instance without user authentication, set up a bots.yaml file as above, but omit the `users` section. Then use the app keyword argument:

````python
import twitter_bot_utils

twitter = twitter_bot_utils.api.API(app='my_app_name', config_file='path/to/config.yaml')

twitter.search(q="Twitter searches don't require user authentication")
````

## Recent tweets

Basically, the `twitter_bot_utils.api.API` object is a wrapper for Tweepy with some configuration reading options added. It also adds three convenience methods for finding recent tweets, since it's often useful to know what a bot has done recently without setting up a whole backend for saving the bot's tweets.

````python
twitter = api.API('MyBotName')

twitter.last_tweet
# id of most recent tweet from MyBotName

twitter.last_reply
# id of most recent reply from MyBotName

twitter.last_retweet
# id of most recent retweet from MyBotName

# Example: what's happened since the last time the bot was active?
twitter.search('#botALLY', since_id=twitter.last_tweet)
````

## Default Command Line Options

Some useful command line flags are available by default:

* `-n, --dry-run`: Don't tweet, just output to stdout
* `-v, --verbose`: Log to stdout
* `-c, --config`: path to a config file. This is a JSON or YAML file laid out according to the below format. 

You can also pass authentication arguments with these arguments.

* `--key`: Twitter user key
* `--secret`: Twitter user secret
* `--consumer-key`: Twitter application consumer key
* `--consumer-secret`: Twitter application consumer secret

Say this is `yourapp.py`:

````python
import argparse
import twitter_bot_utils as tbu

# This sets up an argparse.ArgumentParser with the default arguments
parent = tbu.args.parent()
parser = argparse.ArgumentParser('Description', parents=[parent])
parser.add_argument('-m', '--my-arg')

args = parser.parse_args()

# Set up a logger named 'MyBot'
# Parse the default args. For instance, if --verbose is set, the logger will output to stdout.
# The default arguments include 'verbose', which will enable logger.debug() statements
logger = tbu.args.add_logger('MyBot', args.verbose)

# Generate a tweet somehow
tweet = my_tweet_function(args.my_arg)

twitter = tbu.api.API('MyBot', **vars(args))

logger.info("Generated "+ tweet)

# Use args.dry_run to control tweeting
if not args.dry_run:
    twitter.update_status(tweet)
````

Then on the command line:
````bash
# Looks for settings in a config file (e.g. bots.yaml, see config section above)
# Outputs results to stdout, doesn't publish anything 
$ python yourapp.py --dry-run --verbose
Generated <EXAMPLE TWEET>

# Authenicate with these values instead of the config file
$ python yourapp.py --verbose --consumer-key $ck --consumer-secret $cs --key $user_key --secret $user_secret
Generated <EXAMPLE TWEET 2>
````

## Helpers
### Checking for entities

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

### Filtering out entities

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

### Command Line Utilities
* `twitter-auto-follow`: Follow accounts that follow your bot
* `twitter-fave-mentions`: Favorite your bots' mentions

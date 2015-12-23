# twitter bot utils

Twitter bot utils make it a little easier to set up a Twitter bot, with an eye to making config and command-line options easy to manage and reproduce. They're intended for managing a small-to-medium-sized coterie of Twitter accounts on one machine. The package is a super-simple wrapper for the excellent [Tweepy](http://tweepy.org) library. It also provides shortcuts for setting up command line tools with [argparse](https://docs.python.org/3/library/argparse.html).

This package is intended to assist with the creation of bots for artistic or personal projects. Don't use it to spam or harrass people.

Works with Python 2.7, 3.4 and 3.5 (2.6 & 3.3 probably work, too).

Install with `pip install twitter_bot_utils`.

## Setting up a tweepy API

The main goal of Twitter bot utils is to create Tweepy instances with authentication data stored in a simple conf file. This gives botmakers a simple, reusable place to store keys outside of source control.

By default, `twitter_bot_utils` will read settings from a YAML or JSON config file. By default, it looks in the `~/` and `~/bots` directories for files named "bots.yaml" or "bots.json". Custom config locations can be set, too, of course.

````python
import twitter_bot_utils as tbu

# Automatically check for a config file in the above-named directories
twitter = tbu.API('MyBotName')

# Specify a specific config file
twitter = tbu.API('MyBotName', config_file='path/to/config.yaml')

# This is possible, although you should probably just using Tweepy directly
twitter = tbu.API('MyBotName', consumer_key='...', consumer_secret='...', key='...', secret='...')
````

The `bots` config file is also useful for storing keys and parameters for other APIs, or for your own bots, keep reading!

The `tbu.API` object also extends the `tweepy.API` object with some methods useful for bots:

* Methods to check for the ID of recent tweets: `last_tweet`, `last_reply`, `last_retweet`. These are useful if your bot searches twitter and wants to avoid ingesting the same material.
* A retry in `update_status` when Twitter is over capacity. If `update_status` gets a 503 error from Twitter, it will wait 10 seconds and try again.

Twitter bot utils comes with some built-in command line parsers, and the API object will also happily consume the result of `argparse.parser.parse_args()` (see below for details).

### Config file setup

Custom settings in the config are available at runtime, so use the config file for any special settings you want. (These examples are in YAML, JSON works, too.)

These are two ways to set up a config file. The simple way covers just one user and one app:
````yaml
key: LONGSTRINGOFLETTERS-ANDNUMBERS
secret: LETTERSANDNUMBERS
consumer_key: LOL123...
consumer_secret: OMG456...
my_setting: "bots are good"
````

If you have more than one bot or app, you may find this more involved syntax useful:
````yaml
general_setting: "all bots share this setting"

users:
    # twitter screen_name
    MyBotName:
        key: LONGSTRINGOFLETTERS-ANDNUMBERS
        secret: LETTERSANDNUMBERS
        # The app key should match a key in apps below
        app: my_app_name
        custom_setting: "hello world"

    other_bot:
        key: ...
        secret: ...
        app: my_app_name

apps:
    my_app_name:
        app_setting: "apple juice"
        consumer_key: ...
        consumer_secret: ...
````

TBU will automatically look for a `bots.yaml` in the current directoy, your home directory (`~/`), or `~/bots`. Of course, you can also specify another location or file name.

Using a basic bots.yaml config file:
````python
import twitter_bot_utils as tbu

# Look for simple config in the default places mentioned above:
twitter = tbu.API()

# Get a general config setting. This might be the key for a third-party API
twitter.config['my_setting']
# "bots are good"
```

Using the syntax for multiple bots and apps:
```
twitter = tbu.API(screen_name='MyBotName')

# Use a general setting
twitter.config['general_setting']
# "all bots share this setting"

# Settings from the user and app section are also available:
twitter.config['custom_setting']
# "hello world"

twitter.config['app_setting']
# "apple juice"
````

Set a custom config file with the `config_file` argument:

````python
# The config keyword argument will set a custom file location
twitter = twitter_bot_utils.api.API(screen_name='MyBotName', config_file='special/config.yaml')
````

### Without user authentication

Some Twitter API queries don't require user authentication. To set up an Tweepy API instance without user authentication, set up a bots.yaml file as above, but omit the `users` section. Then use the app keyword argument:

````python
twitter = tbu.API(app='my_app_name', config_file='path/to/config.yaml')

twitter.search(q="Twitter searches don't require user authentication")
````

## Recent tweets

Basically, the `twitter_bot_utils.api.API` object is a wrapper for Tweepy with some configuration reading options added. It also adds three convenience methods for finding recent tweets, since it's often useful to know what a bot has done recently without setting up a whole backend for saving the bot's tweets.

````python
twitter = tbu.API(screen_name='MyBotName')

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

It's useful to package bots as command line apps so that they can be easily run with `cron`. Twitter bot utils includes some helpers for working with `argparse`.

Some useful command line flags are available by default:

* `-u, --user`: Screen name to run as
* `-n, --dry-run`: Don't tweet, just output to stdout
* `-v, --verbose`: Log to stdout
* `-q, --quiet`: Only log errors
* `-c, --config`: path to a config file. This is a JSON or YAML file laid out according to the above format. This option isn't needed if the config file is in one of the default places.

Say this is `yourapp.py`:

````python
import argparse
import twitter_bot_utils as tbu

# This sets up an argparse.ArgumentParser with the default arguments
parent = tbu.args.parent()
parser = argparse.ArgumentParser('My Example Bot', parents=[parent])
parser.add_argument('--my-arg', type=str, help='A custom argument')

args = parser.parse_args()

# Set up the tweepy API
# Note that you can pass the argparse.Namespace object
twitter = tbu.API(args)

# Generate a tweet somehow
tweet = my_tweet_function(args.my_arg)

# The API includes an instance of logging
# debug logs will output to stdout only if --verbose is set
# info logs will output even without --verbose
api.logger.debug("Generated %s", tweet)

# Use args.dry_run to control tweeting
if not args.dry_run:
    try:
        twitter.update_status(tweet)
    except Exception as e:
        # Error logs will go to stdout even when --quiet is set
        logger.error(e)
````

Then on the command line:
````bash
> python yourapp.py --help
usage: yourapp.py [options]

My Example Bot

optional arguments:
  -h, --help            show this help message and exit
  -c PATH, --config PATH
                        bots config file (json or yaml)
  -u SCREEN_NAME, --user SCREEN_NAME
                        Twitter screen name
  -n, --dry-run         Don't actually do anything
  -v, --verbose         Run talkatively
  -q, --quiet           Run quietly
  --my-arg MY_ARG       A custom argument

# Looks for settings in a config file (e.g. bots.yaml, see config section above)
# Prints results to stdout and doesn't publish anything 
> python yourapp.py  --dry-run --verbose
Generated <EXAMPLE TWEET>

# Run quietly, say in a crontab file
> python yourapp.py --user MyBotName --quiet
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
* `auto-follow`: Follow accounts that follow your bot
* `fave-mentions`: Favorite your bot's mentions

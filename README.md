# twitter bot utils

Twitter bot utils make it a little easier to set up a Twitter bot, with an eye to making config and command-line options easy to manage and reproduce. They're intended for managing a small-to-medium-sized coterie of Twitter accounts on one machine. The package is a super-simple wrapper for the excellent [Tweepy](http://tweepy.org) library. It also provides shortcuts for setting up command line tools with [argparse](https://docs.python.org/3/library/argparse.html).

This package is intended to assist with the creation of bots for artistic or personal projects. Don't use it to spam or harrass people.

Works with python 3.4>=. 

Install with `pip install twitter_bot_utils`.

See a basic run through in the [Hello World](https://pythonhosted.org/twitter_bot_utils/helloworld.html) section of the [documentation](https://pythonhosted.org/twitter_bot_utils).

## Authenticating

One hurdle with setting up bots is getting the proper authentication keys. It can be a bit of a pain to log in and out of Twitter's app site. Twitter bot utils comes with `tbu auth`, a command line helper for this:
````
$ tbu auth --consumer-key 1233... --consumer-key 345...
````

This will prompt you with an url. Open this in a browser where your bot is logged in, click "Authorize". Twitter will show you an authorization code, enter this on the command line, and presto! your keys will be displayed.

`tbu auth` is inspired by a feature of [`twurl`](https://github.com/twitter/twurl), Twitter's full-fledged command line tool.

## Config files

One goal of Twitter Bot Utils is to create Tweepy instances with authentication data stored in a simple config file. This gives botmakers a simple, reusable place to store keys outside of source control.

By default, Twitter bot utils looks for a file called `bots.yaml` or `bots.json` in the current directory, your home directory (`~/`) or the `~/bots` directory. Custom config locations can be set, too.

These are two ways to lay out a bots config file. The basic way covers just one user and one app:

````yaml
token: ...
secret: ...
consumer_key: ...
consumer_secret: ...
my_setting: "bots are good"
````

If you have more than one bot, a simple setup is to have one app for each bot. Visit [apps.twitter.com](https://apps.twitter.com), register the app, and then choose "Create my access token" in the "keys and tokens" tab.
````yaml
general_setting: "all bots share this setting"

users:
    # twitter screen_name
    MyBotName:
        token: ...
        secret: ...
        consumer_key: ...
        consumer_secret: ...
        custom_setting: "bots are great"

    other_bot:
        ...
````

If you have one app shared by several bots, create an `apps` section in the config file:
````yaml
apps:
    my_app_name:
        consumer_key: ...
        consumer_secret: ...
users:
    MyBotName:
        token: ...
        secret: ...
        app: my_app_name
````

The `twitter-auth` utility will happily read settings from a `bots.yaml` file set up like this:
````
twitter-auth -c ~/bots.yaml --app my_app_name
````

## Using config files to talk to Twitter

Using a config file in one of the default locations doesn't require any extra settings:

````python
import twitter_bot_utils as tbu

# Automatically check for a config file in the above-named directories
twitter = tbu.API(screen_name='MyBotName')
````

The `twitter` object is a fully-authenticated tweepy API object. So you can now do this:
````python
twitter.update_status(status='hello world')
````

The `bots` config file is also useful for storing keys and parameters for other APIs, or for your own bots.

````python
# Get a config settings from your bots config file. This might be the key for a third-party API
# Use a general setting
twitter.config['general_setting']
# "all bots share this setting"

# Settings from the user and app section are also available:
twitter.config['custom_setting']
# "bots are great"

twitter.config['app_setting']
# "apple juice"
````

Set a custom config file with the `config_file` argument:
````
# Specify a specific config file
twitter = tbu.API(screen_name='MyBotName', config_file='path/to/config.yaml')
````

Twitter bot utils comes with some built-in command line parsers, and the API object will also happily consume the result of `argparse.parser.parse_args()` (see below for details).

### Without user authentication

Some Twitter API queries don't require user authentication. To set up an Tweepy API instance without user authentication, set up a bots.yaml file as above, but omit the `users` section. Use the app keyword argument:
````python
twitter = tbu.API(app='my_app_name', config_file='path/to/config.yaml')

twitter.search(q="Twitter searches don't require user authentication")
````

## Recent tweets

The `twitter_bot_utils.API` object extends `tweepy.API` with some methods useful for bots:

* Methods to check for the ID of recent tweets: `last_tweet`, `last_reply`, `last_retweet`. These are useful if your bot searches twitter and wants to avoid ingesting the same material.

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

Twitter bot utils also adds a retry in `update_status` when Twitter is over capacity. If `update_status` gets a 503 error from Twitter, it will wait 10 seconds and try again.

## Default Command Line Options

It's useful to package bots as command line apps so that they can be easily run with `cron`. Twitter bot utils includes some helpers for working with `argparse`.

Some useful command line flags are available by default:

* `-u, --user`: Screen name to run as
* `-n, --dry-run`: Don't tweet, just output to stdout
* `-v, --verbose`: Log to stdout
* `-q, --quiet`: Only log errors
* `-c, --config`: path to a config file. This is a JSON or YAML file laid out according to the above format. This option isn't needed if the config file is in one of the default places.

Say this is `mybot.py`:

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
    twitter.update_status(tweet)
````

Then on the command line:
````bash
> python mybot.py --help
usage: mybot.py [options]

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
twitter_bot_utils.helpers.has_url
twitter_bot_utils.helpers.has_symbol
````

### Filtering out entities

These helpers remove entities from a tweet's text.

````python
import twitter_bot_utils as tbu

api = tbu.API(screen_name='MyBotName')

results = api.search("special topic")

results[0].text
# 'This is an example tweet with a #hashtag and a link http://foo.com'

tbu.helpers.remove_entity(results[0], 'hashtags')
# 'This is an example tweet with a  and a link http://foo.com'

tbu.helpers.remove_entity(results[0], 'urls')
# 'This is an example tweet with a #hashtag and a link '

# Remove multiple entities with remove_entities.
tbu.helpers.remove_entities(results[0], ['urls', 'hashtags', 'media'])
# 'This is an example tweet with a  and a link '
````

### Command line utilities

Twitter bot utils includes a command line tool with a few useful subcommands:

* `tbu auth`: Authenticate and account with a Twitter app.
* `tbu follow`: Follow accounts that follow your bot
* `tbu like`: Like (aka favorite) your bot's mentions
* `tbu post`: Basic command line for posting text and images

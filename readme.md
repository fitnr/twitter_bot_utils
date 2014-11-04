## twitter bot utils

These Python utilities make it a little easier to set up a Twitter bot, with an eye to making command-line options easy to reproduce.

The utilities are a wrapper for the excellent [Tweepy](http://tweepy.org) and [argparse]() libraries, which handle the Twitter API and command line options, respectively. They're ideal if you want to store the configuration settings for a few bots in a config file.

### Setting up a tweepy API

Easily set up the api with a yaml or json config file:

````python
from twitter_bot_utils import api

# Different ways to create the tweepy API object.
twitter = api.API('MyBotName', config='path/to/config.yaml')
twitter = api.API('MyBotName', consumer_key='...', consumer_secret='...', key='...', secret='...')

# If the config file is set up, twitter bot utils will find it automatically
# See below for details
twitter = api.API('MyBotName')

# twitter_bot_utils comes with some built-in command line parsers, so below.
# It will happily consume the result of argparse.parser.parse_args()
# Assuming a parser has been set up:
args = parser.parse_args()
twitter = api.API('MyBotName', args)
````
### Config file setup

By default, twitter_bot_utils will read settings from a YAML or JSON config file. By default, it looks in the ~/ and ~/bots directories for files named  bots.yaml, bots.json, or botrc. Custom config files can be set, too, of course

Custom settings in the config are available at runtime, so use the config file for any special settings you want.

Example config file layout (in YAML. JSON works, too):

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

Some useful command line flags are available by default:

* -n, --dry-run: Don't tweet, just output to stdout
* -v, --verbose: Log to stdout
* -c, --config: path to a config file. This is a JSON or YAML file laid out according to the below format. 

You can also pass authentication arguments with these options arguments.

* --key: Twitter user key
* --secret: Twitter user secret
* --consumer-key: Twitter application consumer key
* --consumer-secret: Twitter application consumer secret

Say this is `yourapp.py`:

````python
import logging
import twitter_bot_utils

# This sets up an argparse.ArgumentParser with some default arguments, which are explained below
parser = twitter_bot_utils.setup_args('MyBot', description='Tweet something')

parser.add_argument('-m', '--my-arg', help="You're passing an argument to argparse.ArgumentParser")

args = parser.parse_args()

# Parse the default args. If vocal is set, the logger will output to stdout.
twitter_bot_utils.defaults('MyBot', args)

# That's right, utils set up a logger for you.
# It has the same name as the first argument to setup_args
logger = logging.getLogger('MyBot')

# Do logic here to generate a tweet somehow
tweet = my_tweet_function(args.my_arg)

logger.info("Generated "+ tweet)

# Use args.dry_run to control tweeting
if not args.dry_run:
    twitter.update_status(tweet)
````

````bash
# Looks for settings in a config file (e.g. bots.yaml, see config section above)
# Outputs results to stdout, doesn't publish anything 
$ python yourapp.py --dry-run --verbose
Generated <EXAMPLE TWEET>

# Authenicate with these values instead of the config file
$ python yourapp.py --verbose --consumer-key $ck --consumer-secret $cs --key $user_key --secret $user_secret
Generated <EXAMPLE TWEET 2>
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

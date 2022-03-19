0.14
----
* Bump required tweepy to 4.6
* Remove `api.update_status` method with retry
* Remove `use_env` option in API.
* Remove support for bots.json files

0.13
----
* Add `tbu retweet` method to command-line tool
* Boring updates to packaging method and testing
* Remove media upload methods now available in tweepy

0.12.1
------
* Remove remaining Python 2 methods and support (#6)
* Move tests to tox

0.12.0
------
* Remove support for Python 2

0.11.6.post1
------
* Fix bad import in helpers

0.11.6
------
* Add `api.media_upload` method as workaround for old/missing functions in tweepy
* Add `helpers.length` method to get length of text as understood by Twitter
* Change default length on `helpers.chomp` to 280
* Remove explicit support for Tweepy 3.4.0

0.11.5
------
* Fix a bug that would prevent proper return of a Status object with API.update_status in some cases.
* Expand tests to include latest with Tweepy from Github.

0.11.4
------
* Add ability to read auth keys from environment variables: TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_KEY, TWITTER_SECRET

0.11.2
------
* Fixes and expands `tbu auth` interface (issues #4 and #5)
* Allow install for a greater range of twitter_bot_utils versions

0.11.1
------

* Remove (no)header option.

0.11.0
------

* Consolidated command line tools to subcommands of `tbu`. Added deprecation warnings to earlier versions of commands.
* Add (no)header option to archive reading.

0.10.5
------

* Fix encoding bug when reading non-ASCII text from archives.
* Add docs

0.10.4
------
* Add `include` argument to `args.parent`
* Bump required `tweepy` to take advantage of `TweepError.api_code`
* In Py 3, don't read config files as strings, not bytes
* Check rate limits in follow/fave tools

0.10.3
------
* Simplify config section
* Add twitter-auth command line tool

0.10.post1
------
* Fix missing handler on `API.logger`.
* Change internal api for logger, now accepts a `logging` level.

0.10.0
------
* Add `helpers.chomp` method for progressively shortening strings.
* Remove app, secret, consumer-key and consumer-secret command line args. A bots.yaml config file now mandatory.
* No longer urlencode when queryizing
* Logging: Remove file logger, add silent option, start logger with args, add logger in api
* Rename helper utils to 'auto-follow' and 'fave-mentions'

0.9.7
-----
* Fix py3 error on reading archives

0.9.6
-----
* Look farther back when picking recent tweets

0.9.5.1
-------

* Fix a little bug in the `archive.read_csv` api. Now accepts directories or paths.

0.9.5
-----

* Add abilty to read Twitter csv archive files with `archive.read_csv`

0.9.1.post1
-----------

* OK, we don't want universal builds, whoops.

0.9.1
-----

* Fixed Windows bug (thanks hugovk)
* Added mock to tests, using Travis for CI
* Smoother Python 2/3 integration

0.9
-----

* Setup easier for tasks that don't require Twitter authentication
* Big update to follow/fave CLI
* Added tox and various tests
* Refactored args module

0.8.1
-----

* Overhaul command line follow/favorite utilities
* Fix imports in Py3
* Expand tests

0.8
-----
* No longer accept argpase.Namespace in api.API. use keyword args instead.

0.7
-----

* Change api for creating parsers. `creation` module is gone, use tbu.args.parent() to pass a parent to `argparse.ArgumentParser`.

0.6.6
-----

* Grab longer user timeline for establishing recent replies, retweets

0.6.5
-----

* Fix bugs in queryize, recent tweets in API
* use logger named screen_name in follow tools

0.6.4
-----

* Add helpers.queryize - formats a list of terms for a Twitter search.
* Automatically use ellipsis character ('…') in helpers.shorten when `ellipsis=True`.


0.6.3
-----

* Add helpers.shorten - cuts a string down to 140 characters without breaking words.

0.6.2
-----

Add 'archive' module for reading Twitter archives or simple text files.


0.6.1
-----

Typos

0.6
---

* Add confighelper module, with tools for parsing simple config files
* Fix Python 3 compatibility

0.5.2
-----

Changes:

* Add helpers.replace_urls method

0.5
---

Changes:

* Release into the wild
* Simplify config getting and setting when creating api.API
* Import with api.API, instead of API living in __all__
* Simplify error-throwing
* Find handling of bad configs
* Update docs

0.4
---

Changes:

* Add test cases
* Move tools to tools.py
* Add test formatting
* Update docs
* Add entity filters

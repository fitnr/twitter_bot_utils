0.9.8
-----
* Add `helpers.chomp` method for progressively shortening strings.

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
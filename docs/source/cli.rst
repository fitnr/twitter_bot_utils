Command line tools
==================

Twitter Bot Utils comes with the ``tbu`` command line tool, which has several subcommands:

- tbu auth
- tbu follow
- tbu like
- tbu post

tbu auth
------------

::

    usage: tbu auth [-h] [-c file] [--app app] [-s] [--consumer-key key]
                        [--consumer-secret secret] [-V]

    Authorize an account with a twitter application.

    optional arguments:
      -h, --help            show this help message and exit
      -c file               config file
      --app app             app name in config file
      -s, --save            Save details to config file
      --consumer-key key    consumer key (aka consumer token)
      --consumer-secret secret
                            consumer secret
      -V, --version         show program's version number and exit

tbu follow
-----------

::

    usage: tbu follow [options] screen_name

    automatic following and unfollowing

    positional arguments:
      screen_name

    optional arguments:
      -h, --help            show this help message and exit
      -U, --unfollow        Unfollow those who don't follow you
      -c PATH, --config PATH
                            bots config file (json or yaml)
      -n, --dry-run         Don't actually do anything
      -v, --verbose         Run talkatively
      -q, --quiet           Run quietly
      -V, --version         show program's version number and exit

tbu like
--------

::

    usage: tbu like [options] screen_name

    fave/like mentions

    positional arguments:
      screen_name

    optional arguments:
      -h, --help            show this help message and exit
      -c PATH, --config PATH
                            bots config file (json or yaml)
      -n, --dry-run         Don't actually do anything
      -v, --verbose         Run talkatively
      -q, --quiet           Run quietly
      -V, --version         show program's version number and exit


tbu post
--------

::

    usage: tbu post screen_name "update" [options]

    Post text to a given twitter account

    positional arguments:
      screen_name
      update

    optional arguments:
      -h, --help            show this help message and exit
      -m MEDIA_FILE, --media-file MEDIA_FILE
      -c PATH, --config PATH
                            bots config file (json or yaml)
      -n, --dry-run         Don't actually do anything
      -v, --verbose         Run talkatively
      -q, --quiet           Run quietly

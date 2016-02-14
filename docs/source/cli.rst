Command line tools
==================

Twitter Bot Utils comes with three command line tools:

- fave-mentions
- auto-follow
- twitter-auth

fave-mentions
-------------

.. code:: bash

    usage: fave-mentions [options] screen_name

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

auto-follow
-----------

.. code:: bash

    usage: auto-follow [options] screen_name

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

twitter-auth
------------

.. code:: bash

    usage: twitter-auth [-h] [-c file] [--app app] [-s] [--consumer-key key]
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

Hello World
===========

The first step of any bot is to set up an app and a new account. Those steps
are an exercise for the reader.

Twitter Bot Utils is opinionated about one thing: it wants you to store authentication
keys in a file called ``~/bots.yaml`` or ``~/bots.json``. (It's actually not that opinionated
about where the file goes, read on.)

If you're using a YAML file, it should look like this:

.. code:: yaml

    apps:
        my_app_name:
            consumer_key: LONGSTRINGOFLETTERS-ANDNUMBERS
            consumer_secret: LETTERSANDNUMBERS
    users:
        # twitter screen_name
        MyBotName:
            key: LONGSTRINGOFLETTERS-ANDNUMBERS
            secret: LETTERSANDNUMBERS
            # The app key should match a key in apps below
            app: my_app_name

    
Wait, we haven't authenticated the account with the app. Let's do that quickly
with the Twitter Bot Utils ``twitter-auth`` command:

.. code:: bash
    
    $ twitter-auth --app my_app_name
    https://api.twitter.com/oauth/authorize?oauth_token=dWXqSAAAAAAALgurAAABUuIOe0c
    Please visit this url, click "Authorize app" and enter in the PIN:
    >


Now visit the URL in your favorite browser, authorize the app, and you'll be rewarded with
key and secret, which you can place in ``bots.yaml``.

Next, create a python file called ``my_twitter_bot.py`` that looks like this:

.. code:: python

    import argparse
    import twitter_bot_utils as tbu

    def main():
        parser = argparse.ArgumentParser(description='my twitter bot')
        tbu.args.add_default_args(parser, version='1.0')

        args = parser.parse_args()
        api = tbu.api.API(args.user)

        if not args.dry_run:
            api.update_status('Hello World!')
            api.logger.info('I just tweeted!')

    if __name__ == '__main__':
        main()


On the command line, this will create a full-fledged app that will have lots of tricks:

.. code:: bash
    
    $ python my_twitter_bot.py --help
    usage: my_twitter_bot.py [-h] [-c PATH] [-n] [-v] [-q] [-V] [-u screen_name]

    my twitter bot

    optional arguments:
      -h, --help            show this help message and exit
      -c PATH, --config PATH
                            bots config file (json or yaml)
      -n, --dry-run         Don't actually do anything
      -v, --verbose         Run talkatively
      -q, --quiet           Run quietly
      -V, --version         show program's version number and exit


To tweet, run this:

.. code:: bash

    $ python my_twitter_bot.py -u MyBotName
    I just tweeted!

Now you can go ahead and add this command to ``cron``, and you're good to go!

Another approach
----------------

Create the ``bots.yaml`` file as above, but when creating your bot, just set it to print a tweet:

.. code:: python

   def main():
       print('This is a tweet!')

    if __name__ == '__main__':
        main()

Now, pipe your scripts output to the ``tbu post`` command:

.. code:: bash

    $ python3 my_twitter_bot.py | tbu post MyBotName

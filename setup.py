from setuptools import setup

setup(
    name='twitter_bot_utils',

    version='0.4.0',

    description='Python utilities for twitter bots',

    url='http://github.com/fitnr/twitter_bot_utils',

    author='Neil Freeman',

    author_email='contact@fakeisthenewreal.org',

    license='All rights reserved',

    packages=['twitter_bot_utils'],

    entry_points={
        'console_scripts': [
            'fave_mentions=twitter_bot_utils.tools:cli_fave_mentions',
            'auto_follow=twitter_bot_utils.tools:cli_auto_follow'
        ],
    },

    install_requires=[
        'tweepy>=2.3.0',
        'PyYAML>=3.11',
        'argparse>=1.2.1',
    ],

)

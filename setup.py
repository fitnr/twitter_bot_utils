from setuptools import setup
from twitter_bot_utils import __version__
setup(
    name='twitter_bot_utils',

    version=__version__,

    description='Python utilities for twitter bots',

    long_description=open('readme.rst', 'r').read(),

    url='http://github.com/fitnr/twitter_bot_utils',

    author='Neil Freeman',

    author_email='contact@fakeisthenewreal.org',

    license='GPLv3',

    packages=['twitter_bot_utils'],

    entry_points={
        'console_scripts': [
            'twitter-fave-mentions=twitter_bot_utils.cli:fave_mentions',
            'twitter-auto-follow=twitter_bot_utils.cli:auto_follow'
        ],
    },

    use_2to3=True,

    install_requires=[
        'tweepy >=3.1.0, <4',
        'PyYAML==3.11',
        'argparse>=1.2.1',
    ],
    test_suite='tests'
)

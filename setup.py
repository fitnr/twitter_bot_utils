from setuptools import setup

try:
    readme = open('./README.rst', 'r').read()
except IOError:
    readme = ''

setup(
    name='twitter_bot_utils',

    version='0.10.post1',

    description='Python utilities for twitter bots',

    long_description=readme,

    url='http://github.com/fitnr/twitter_bot_utils',

    author='Neil Freeman',

    author_email='contact@fakeisthenewreal.org',

    license='GPL-3.0',

    packages=['twitter_bot_utils'],

    entry_points={
        'console_scripts': [
            'fave-mentions=twitter_bot_utils.cli:fave_mentions',
            'auto-follow=twitter_bot_utils.cli:auto_follow'
        ],
    },

    use_2to3=True,

    install_requires=[
        'tweepy >=3.1.0, <4',
        'PyYAML==3.11',
        'argparse>=1.1',
    ],

    test_suite="tests",

    tests_require=[
        'coverage',
        'mock'
    ],
)

from setuptools import setup

try:
    readme = open('./README.rst', 'r').read()
except IOError:
    readme = ''

with open('twitter_bot_utils/__init__.py') as i:
    version = next(r for r in i.readlines() if '__version__' in r).split('=')[1].strip('"\' \n')

setup(
    name='twitter_bot_utils',

    version=version,

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
            'auto-follow=twitter_bot_utils.cli:auto_follow',
            'twitter-auth=twitter_bot_utils.cli:authenticate',
            'tbu=twitter_bot_utils.cli:main',
        ],
    },

    use_2to3=True,

    install_requires=[
        'tweepy >=3.4.0, <4',
        'PyYAML==3.11',
    ],

    test_suite="tests",

    tests_require=[
        'coverage',
        'mock',
        'sphinx',
        'sphinx_rtd_theme'
    ],
)

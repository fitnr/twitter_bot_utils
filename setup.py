from setuptools import setup

try:
    from pypandoc import convert
    def read_md(f):
        try:
            return convert(f, 'rst')
        except IOError:
            return ''

except ImportError:
    print("pypandoc module not found, could not convert Markdown to RST")
    def read_md(f):
        try:
            return open(f, 'r').read()
        except IOError:
            return ''


setup(
    name='twitter_bot_utils',

    version='0.6.4',

    description='Python utilities for twitter bots',

    long_description=read_md('readme.md'),

    url='http://github.com/fitnr/twitter_bot_utils',

    author='Neil Freeman',

    author_email='contact@fakeisthenewreal.org',

    license='GPL',

    packages=['twitter_bot_utils'],

    entry_points={
        'console_scripts': [
            'fave_mentions=twitter_bot_utils.tools:cli_fave_mentions',
            'auto_follow=twitter_bot_utils.tools:cli_auto_follow'
        ],
    },

    use_2to3=True,

    install_requires=[
        'tweepy >=3.1.0, <4',
        'PyYAML==3.11',
        'argparse>=1.2.1',
    ],

)

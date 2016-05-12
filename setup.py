# Copyright 2014-2016 Neil Freeman contact@fakeisthenewreal.org
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
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

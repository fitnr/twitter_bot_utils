#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import unittest

from twitter_bot_utils import confighelper


class test_confighelper(unittest.TestCase):
    # pylint: disable=invalid-name
    screen_name = 'example_screen_name'

    def setUp(self):
        self.datapath = os.path.join(os.path.dirname(__file__), 'data')
        self.yaml = os.path.join(self.datapath, 'test.yaml')
        self.json = os.path.join(self.datapath, 'test.json')
        self.simple = os.path.join(self.datapath, 'simple.yml')
        self.badfile = os.path.join(self.datapath, 'tweets.txt')

    def testDefaultDirs(self):
        self.assertIn('~', confighelper.CONFIG_DIRS)

    def test_find_file(self):
        for f in (self.simple, self.yaml, self.json):
            self.assertEqual(f, confighelper.find_file(f))
            self.assertEqual(
                f, confighelper.find_file(default_bases=(os.path.basename(f),), default_directories=[self.datapath])
            )

    def test_yaml(self):
        config = confighelper.configure(self.screen_name, config_file=self.yaml)
        self.assertEqual(config['key'], 'INDIA')
        self.assertEqual(config["consumer_key"], "NOVEMBER")

    def test_json(self):
        config = confighelper.configure(self.screen_name, config_file=self.json)
        self.assertEqual(config['key'], 'INDIA')
        self.assertEqual(config["consumer_key"], "NOVEMBER")

    def test_simple(self):
        config = confighelper.configure(config_file=self.simple)
        self.assertEqual(config['key'], 'INDIA')
        self.assertEqual(config["consumer_key"], "NOVEMBER")

    def test_parse(self):
        with self.assertRaises(ValueError):
            confighelper.parse('foo.unknown')

        with self.assertRaises((IOError, OSError)):
            confighelper.parse('unknown.json')

    def testConfigKwargPassing(self):
        conf = confighelper.parse(self.yaml)
        config = confighelper.configure(config_file=self.yaml, **conf)
        assert conf['custom'] == config['custom']

    def testConfigKwargPassingJSON(self):
        conf = confighelper.parse(self.json)
        config = confighelper.configure(config_file=self.json, **conf)
        assert conf['custom'] == config['custom']

    def testConfigBadFileType(self):
        with self.assertRaises(ValueError):
            confighelper.parse(self.badfile)

    def testDumpConfig(self):
        conf = confighelper.parse(self.json)
        sink = 'a.json'
        confighelper.dump(conf, sink)

        dumped = confighelper.parse(sink)

        assert dumped['custom'] == conf['custom']
        assert 'users' in dumped

        os.remove(sink)

    def testDumpConfigBadFileType(self):
        with self.assertRaises(ValueError):
            confighelper.dump({}, 'foo.whatever')

    def testMissingConfig(self):
        with self.assertRaises(Exception):
            confighelper.find_file('imaginary.yaml', (os.path.dirname(__file__),))

    def test_config_setup(self):
        config = confighelper.configure(self.screen_name, config_file=self.yaml, random='foo')

        assert config['secret'] == 'LIMA'
        assert config['consumer_key'] == 'NOVEMBER'
        assert config['random'] == 'foo'

    def testSimpleConfig(self):
        config = confighelper.configure(config_file=self.simple, random='foo')
        assert config['secret'] == 'LIMA'
        assert config['consumer_key'] == 'NOVEMBER'
        assert config['random'] == 'foo'


if __name__ == '__main__':
    unittest.main()

import unittest

import core.config

class config(unittest.TestCase):
    def setUp(self):
        self.someModules = [ 'b', 'x', 'a' ]
        self.moreModules = [ 'this', 'module', 'here' ]
        self.someTheme = 'some-theme'
        self.someIconset = 'some-iconset'

    def test_module(self):
        cfg = core.config.Config([ '-m' ] + self.someModules)
        self.assertEqual(self.someModules, cfg.modules())

    def test_module_ordering_maintained(self):
        cfg = core.config.Config([ '-m' ] + self.someModules + [ '-m' ] + self.moreModules)
        self.assertEqual(self.someModules + self.moreModules, cfg.modules())

    def test_default_interval(self):
        cfg = core.config.Config([])
        self.assertEqual(1, cfg.interval())

    def test_interval(self):
        cfg = core.config.Config([ '-p', 'interval=4'])
        self.assertEqual(4, cfg.interval())

    def test_float_interval(self):
        cfg = core.config.Config([ '-p', 'interval=0.5'])
        self.assertEqual(0.5, cfg.interval())

    def test_default_theme(self):
        cfg = core.config.Config([])
        self.assertEqual('default', cfg.theme())

    def test_theme(self):
        cfg = core.config.Config(['-t', self.someTheme])
        self.assertEqual(self.someTheme, cfg.theme())

    def test_default_iconset(self):
        cfg = core.config.Config([])
        self.assertEqual('auto', cfg.iconset())

    def test_iconset(self):
        cfg = core.config.Config(['-i', self.someIconset])
        self.assertEqual(self.someIconset, cfg.iconset())

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

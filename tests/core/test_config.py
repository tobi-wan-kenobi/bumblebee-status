import unittest

import core.config

class config(unittest.TestCase):
    def setUp(self):
        self._someModules = [ 'b', 'x', 'a' ]
        self._moreModules = [ 'this', 'module', 'here' ]

    def tearDown(self):
        pass

    def test_module(self):
        cfg = core.config.Config([ '-m' ] + self._someModules)
        self.assertEqual(self._someModules, cfg.modules())

    def test_module_ordering_maintained(self):
        cfg = core.config.Config([ '-m' ] + self._someModules + [ '-m' ] + self._moreModules)
        self.assertEqual(self._someModules + self._moreModules, cfg.modules())

    def test_default_interval(self):
        cfg = core.config.Config([])
        self.assertEqual(1, cfg.interval())

    def test_interval(self):
        cfg = core.config.Config([ '-p', 'interval=4'])
        self.assertEqual(4, cfg.interval())

    def test_float_interval(self):
        cfg = core.config.Config([ '-p', 'interval=0.5'])
        self.assertEqual(0.5, cfg.interval())

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

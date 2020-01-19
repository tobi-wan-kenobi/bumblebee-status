import unittest

import core.config

class config(unittest.TestCase):
    def setUp(self):
        self._someModules = [ 'b', 'x', 'a' ]
        self._moreModules = [ 'this', 'module', 'here' ]

    def tearDown(self):
        pass

    def test_module_parameter(self):
        cfg = core.config.Config([ '-m' ] + self._someModules)
        self.assertEqual(self._someModules, cfg.modules())

    def test_module_parameter_ordering_maintained(self):
        cfg = core.config.Config([ '-m' ] + self._someModules + [ '-m' ] + self._moreModules)
        self.assertEqual(self._someModules + self._moreModules, cfg.modules())

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

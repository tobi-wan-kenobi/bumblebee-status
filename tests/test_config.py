import unittest

from bumblebee.config import Config

class TestConfig(unittest.TestCase):
    def setUp(self):
        self.defaultConfig = Config()
        self.someSimpleModules = [ "foo", "bar", "baz" ]

    def test_no_modules_by_default(self):
        self.assertEquals(self.defaultConfig.modules(), [])

    def test_load_simple_modules(self):
        cfg = Config([ "-m" ] + self.someSimpleModules)
        self.assertEquals(cfg.modules(), 
            map(lambda x: { "name": x, "module": x }, self.someSimpleModules))

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

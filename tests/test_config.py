import unittest

from bumblebee.config import Config

class TestConfig(unittest.TestCase):
    def setUp(self):
        self.defaultConfig = Config()
        self.someSimpleModules = [ "foo", "bar", "baz" ]
        self.someAliasModules = [ "foo:a", "bar:b", "baz:c" ]


    def test_no_modules_by_default(self):
        self.assertEquals(self.defaultConfig.modules(), [])

    def test_load_simple_modules(self):
        cfg = Config([ "-m" ] + self.someSimpleModules)
        self.assertEquals(cfg.modules(), list(map(lambda x: {
            "name": x, "module": x
        }, self.someSimpleModules)))

    def test_load_alias_modules(self):
        cfg = Config([ "-m" ] + self.someAliasModules)
        self.assertEquals(cfg.modules(), list(map(lambda x: {
            "module": x.split(":")[0],
            "name": x.split(":")[1]
        }, self.someAliasModules)))

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# pylint: disable=C0103,C0111
import unittest

from bumblebee.config import Config

class TestConfig(unittest.TestCase):
    def setUp(self):
        self.defaultConfig = Config()
        self.someSimpleModules = ["foo", "bar", "baz"]
        self.someAliasModules = ["foo:a", "bar:b", "baz:c"]

    def test_no_modules_by_default(self):
        self.assertEquals(self.defaultConfig.modules(), [])

    def test_simple_modules(self):
        cfg = Config(["-m"] + self.someSimpleModules)
        self.assertEquals(cfg.modules(), [{
            "name": x, "module": x
        } for x in self.someSimpleModules])

    def test_alias_modules(self):
        cfg = Config(["-m"] + self.someAliasModules)
        self.assertEquals(cfg.modules(), [{
            "module": x.split(":")[0],
            "name": x.split(":")[1],
        } for x in self.someAliasModules])

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

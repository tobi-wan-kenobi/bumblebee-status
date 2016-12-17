# pylint: disable=C0103,C0111

import unittest
import mock
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from bumblebee.config import Config
from bumblebee.theme import themes
from bumblebee.engine import all_modules

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

    @mock.patch("sys.stdout", new_callable=StringIO)
    @mock.patch("sys.exit")
    def test_list_themes(self, exit, stdout):
        cfg = Config(["-l", "themes"])
        result = stdout.getvalue()
        for theme in themes():
            self.assertTrue(theme in result)

    @mock.patch("sys.stdout", new_callable=StringIO)
    @mock.patch("sys.exit")
    def test_list_modules(self, exit, stdout):
        cfg = Config(["-l", "modules"])
        result = stdout.getvalue()
        for module in all_modules():
            self.assertTrue(module["name"] in result)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# pylint: disable=C0103,C0111,W0703

import unittest
from bumblebee.theme import Theme
from bumblebee.error import ThemeLoadError
from tests.util import MockWidget

class TestTheme(unittest.TestCase):
    def setUp(self):
        self.nonexistentThemeName = "no-such-theme"
        self.invalidThemeName = "invalid"
        self.validThemeName = "solarized-powerline"
        self.someWidget = MockWidget("foo")

    def test_load_valid_theme(self):
        try:
            Theme(self.validThemeName)
        except Exception as e:
            self.fail(e)

    def test_load_nonexistent_theme(self):
        with self.assertRaises(ThemeLoadError):
            Theme(self.nonexistentThemeName)

    def test_load_invalid_theme(self):
        with self.assertRaises(ThemeLoadError):
            Theme(self.invalidThemeName)

    def test_prefix(self):
        theme = Theme(self.validThemeName)
        theme.loads('{"defaults": { "prefix": "test" }}')
        self.assertEquals(theme.prefix(self.someWidget), "test")

    def test_suffix(self):
        theme = Theme(self.validThemeName)
        theme.loads('{"defaults": { "suffix": "test" }}')
        self.assertEquals(theme.suffix(self.someWidget), "test")

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

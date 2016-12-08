# pylint: disable=C0103,C0111,W0703

import unittest
from bumblebee.theme import Theme
from bumblebee.error import ThemeLoadError

class TestTheme(unittest.TestCase):
    def setUp(self):
        self.nonexistentThemeName = "no-such-theme"
        self.invalidThemeName = "invalid"

    def test_load_valid_theme(self):
        try:
            Theme("solarized-powerline")
        except Exception as e:
            self.fail(e)

    def test_load_nonexistent_theme(self):
        with self.assertRaises(ThemeLoadError):
            Theme(self.nonexistentThemeName)

    def test_load_invalid_theme(self):
        with self.assertRaises(ThemeLoadError):
            Theme(self.invalidThemeName)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

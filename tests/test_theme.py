# pylint: disable=C0103,C0111,W0703

import unittest
from bumblebee.theme import Theme
from bumblebee.error import ThemeLoadError
from tests.util import MockWidget

class TestTheme(unittest.TestCase):
    def setUp(self):
        self.nonexistentThemeName = "no-such-theme"
        self.invalidThemeName = "invalid"
        self.validThemeName = "test"
        self.someWidget = MockWidget("foo")
        self.theme = Theme(self.validThemeName)

        self.widgetTheme = "test-widget"
        self.defaultColor = "#000000"
        self.defaultBgColor = "#111111"
        self.widgetBgColor = "#222222"
        self.defaultPrefix = "default-prefix"
        self.defaultSuffix = "default-suffix"
        self.widgetPrefix = "widget-prefix"
        self.widgetSuffix = "widget-suffix"
        self.widgetColor = "#ababab"

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

    def test_default_prefix(self):
        self.assertEquals(self.theme.prefix(self.someWidget), self.defaultPrefix)

    def test_default_suffix(self):
        self.assertEquals(self.theme.suffix(self.someWidget), self.defaultSuffix)

    def test_widget_prefix(self):
        self.someWidget.module = self.widgetTheme
        self.assertEquals(self.theme.prefix(self.someWidget), self.widgetPrefix)

    def test_widget_fg(self):
        self.assertEquals(self.theme.fg(self.someWidget), self.defaultColor)
        self.someWidget.module = self.widgetTheme
        self.assertEquals(self.theme.fg(self.someWidget), self.widgetColor)

    def test_widget_bg(self):
        self.assertEquals(self.theme.bg(self.someWidget), self.defaultBgColor)
        self.someWidget.module = self.widgetTheme
        self.assertEquals(self.theme.bg(self.someWidget), self.widgetBgColor)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

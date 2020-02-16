import unittest

import core.theme

class theme(unittest.TestCase):
    def setUp(self):
        self.invalidThemeName = 'this-theme-does-not-exist'
        self.validThemeName = 'default'
        self.defaultsTheme = {
            'defaults': {
                'fg': 'red', 'bg': 'black'
            }
        }
        self.cycleTheme = {
            'cycle': [
                { 'fg': 'red', 'bg': 'black' },
                { 'fg': 'black', 'bg': 'red' }
            ]
        }

    def test_invalid_theme(self):
        with self.assertRaises(RuntimeError):
            core.theme.Theme(self.invalidThemeName)

    def test_valid_theme(self):
        theme = core.theme.Theme(self.validThemeName)
        self.assertEqual(self.validThemeName, theme.name)

    def test_defaults(self):
        theme = core.theme.Theme(raw_data=self.defaultsTheme)
        self.assertEqual(self.defaultsTheme['defaults']['fg'], theme.fg())
        self.assertEqual(self.defaultsTheme['defaults']['bg'], theme.bg())

    def test_cycle(self):
        theme = core.theme.Theme(raw_data=self.cycleTheme)
        self.assertEqual(self.cycleTheme['cycle'][0]['fg'], theme.fg())
        self.assertEqual(self.cycleTheme['cycle'][0]['bg'], theme.bg())

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

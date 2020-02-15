import unittest

import core.theme

class theme(unittest.TestCase):
    def setUp(self):
        self.invalidThemeName = 'this-theme-does-not-exist'
        self.validThemeName = 'default'
        self.defaults = {
            'defaults': {
                'fg': 'red', 'bg': 'black'
            }
        }

    def test_invalid_theme(self):
        with self.assertRaises(RuntimeError):
            core.theme.Theme(self.invalidThemeName)

    def test_valid_theme(self):
        theme = core.theme.Theme(self.validThemeName)
        self.assertEqual(self.validThemeName, theme.name)

    def test_defaults(self):
        theme = core.theme.Theme(raw_data=self.defaults)
        self.assertEqual(self.defaults['defaults']['fg'], theme.fg())
        self.assertEqual(self.defaults['defaults']['bg'], theme.bg())

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

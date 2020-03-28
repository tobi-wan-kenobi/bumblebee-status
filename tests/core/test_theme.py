import unittest

import core.theme
import core.event

class theme(unittest.TestCase):
    def setUp(self):
        core.event.clear()
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
                { 'fg': 'black', 'bg': 'red' },
                { 'fg': 'white', 'bg': 'blue' }
            ]
        }
        self.colorTheme = {
            'colors': [{
                'red': '#ff0000', 'blue': '#0000ff'
            }]
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
        self.assertEqual(None, theme.bg('previous'))
        self.assertEqual(self.cycleTheme['cycle'][0]['fg'], theme.fg())
        self.assertEqual(self.cycleTheme['cycle'][0]['bg'], theme.bg())
        core.event.trigger('next-widget')
        self.assertEqual(self.cycleTheme['cycle'][0]['bg'], theme.bg('previous'))
        core.event.trigger('next-widget')
        self.assertEqual(self.cycleTheme['cycle'][2]['fg'], theme.fg())
        self.assertEqual(self.cycleTheme['cycle'][2]['bg'], theme.bg())
       
        with unittest.mock.patch('core.output.sys.stdout'):
            core.event.trigger('update')
            self.assertEqual(self.cycleTheme['cycle'][0]['fg'], theme.fg())
            self.assertEqual(self.cycleTheme['cycle'][0]['bg'], theme.bg())

    def test_custom_iconset(self):
        theme = core.theme.Theme(raw_data=self.defaultsTheme)
        self.assertNotEqual('aaa', theme.padding())
        theme = core.theme.Theme(raw_data=self.defaultsTheme, iconset={
            'defaults': { 'padding': 'aaa' }
        })
        self.assertEqual('aaa', theme.padding())

    def test_colors(self):
        theme = core.theme.Theme(raw_data=self.defaultsTheme)
        self.assertEqual({}, theme.keywords())
        theme = core.theme.Theme(raw_data=self.colorTheme)
        self.assertEqual(self.colorTheme['colors'][0], theme.keywords())

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

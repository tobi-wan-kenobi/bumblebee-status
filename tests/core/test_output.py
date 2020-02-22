import json
import unittest

import core.output
import core.module

class TestModule(core.module.Module):
    pass

class i3(unittest.TestCase):
    def setUp(self):
        self.i3 = core.output.i3()
        widget = unittest.mock.MagicMock()
        widget.full_text.return_value = "test"
        self.someModule = TestModule(widgets=[widget, widget, widget])

    def test_start(self):
        core.event.clear()

        all_data = self.i3.start()
        data = all_data['data']
        self.assertEqual(1, data['version'], 'i3bar protocol version 1 expected')
        self.assertTrue(data['click_events'], 'click events should be enabled')
        self.assertEqual('\n[', all_data['suffix'])

    def test_stop(self):
        self.assertEqual('\n]', self.i3.stop()['suffix'], 'wrong i3bar protocol during stop')

    def test_no_modules_by_default(self):
        self.assertEqual(0, len(self.i3.modules()), 'module list should be empty by default')

    def test_register_single_module(self):
        self.i3.modules(self.someModule)
        self.assertEqual(1, len(self.i3.modules()), 'setting single module does not work')

    def test_register_multiple_modules(self):
        self.i3.modules([ self.someModule, self.someModule, self.someModule ])
        self.assertEqual(3, len(self.i3.modules()), 'setting module list does not work')

    def test_draw_existing_module(self):
        self.i3.test_draw = unittest.mock.MagicMock(return_value={
            'data': { 'test': True }, 'suffix': 'end'
        })
        self.i3.draw('test_draw')
        self.i3.test_draw.assert_called_once_with()

    def test_empty_status_line(self):
        data = self.i3.statusline()
        self.assertEqual([], data['data'], 'expected empty list of status line entries')
        self.assertEqual(',', data['suffix'], 'expected "," as suffix')

    def test_statusline(self):
        self.i3.modules([ self.someModule, self.someModule, self.someModule ])
        self.i3.update()
        data = self.i3.statusline()
        self.assertEqual(len(self.someModule.widgets())*3, len(data['data']), 'wrong number of widgets')

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

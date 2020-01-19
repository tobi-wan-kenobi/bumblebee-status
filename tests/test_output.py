import unittest
import json

import core.output

class i3(unittest.TestCase):
    def setUp(self):
        self.i3 = core.output.i3()

    def tearDown(self):
        pass

    def test_start(self):
        data = json.loads(self.i3.start())
        self.assertEqual(1, data['version'], 'i3bar protocol version 1 expected')
        self.assertTrue(data['click_events'], 'click events should be enabled')

    def test_begin_status_line(self):
        self.assertEqual('[', self.i3.begin_status_line(), 'each line must be a JSON array')

    def test_end_status_line(self):
        self.assertEqual('],\n', self.i3.end_status_line(), 'each line must terminate properly')

    def test_stop(self):
        self.assertEqual(']\n', self.i3.stop())

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

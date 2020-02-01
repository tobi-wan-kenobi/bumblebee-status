import unittest
import json

import core.output

class i3(unittest.TestCase):
    def setUp(self):
        self.i3 = core.output.i3()

    def tearDown(self):
        pass

    def test_start(self):
        all_data = self.i3.start()
        data = all_data['data']
        self.assertEqual(1, data['version'], 'i3bar protocol version 1 expected')
        self.assertTrue(data['click_events'], 'click events should be enabled')
        self.assertEqual('\n[', all_data['suffix'])

    def test_stop(self):
        self.assertEqual('\n]', self.i3.stop()['suffix'])

    # TODO: mock a "draw" call

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

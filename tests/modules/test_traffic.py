import mock
import unittest

import tests.mocks as mocks

from bumblebee.modules.traffic import Module

class TestTrafficModule(unittest.TestCase):
    def setUp(self):
        mocks.setup_test(self, Module)

    def test_default_format(self):
        self.assertEqual(self.module._format, "{:.2f}")

    def test_get_minwidth_str(self):
        # default value (two digits after dot)
        self.assertEqual(self.module.get_minwidth_str(), "1000.00KiB/s")
        # integer value
        self.module._format = "{:.0f}"
        self.assertEqual(self.module.get_minwidth_str(), "1000KiB/s")
        # just one digit after dot
        self.module._format = "{:.1f}"
        self.assertEqual(self.module.get_minwidth_str(), "1000.0KiB/s")

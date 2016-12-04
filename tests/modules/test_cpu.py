# pylint: disable=C0103,C0111

import unittest

from bumblebee.modules.cpu import Module
from tests.util import assertWidgetAttributes

class TestCPUModule(unittest.TestCase):
    def setUp(self):
        self.module = Module(None)

    def test_widgets(self):
        widget = self.module.widgets()
        assertWidgetAttributes(self, widget)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

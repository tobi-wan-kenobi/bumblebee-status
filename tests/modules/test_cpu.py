# pylint: disable=C0103,C0111

import unittest

from bumblebee.modules.cpu import Module
from tests.util import assertWidgetAttributes

class TestCPUModule(unittest.TestCase):
    def setUp(self):
        self.module = Module(None)

    def test_widgets(self):
        widgets = self.module.widgets()
        for widget in widgets:
            assertWidgetAttributes(self, widget)

    def test_update(self):
        widgets = self.module.widgets()
        self.module.update(widgets)
        self.test_widgets()
        self.assertEquals(widgets, self.module.widgets())

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

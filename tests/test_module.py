# pylint: disable=C0103,C0111,W0703

import unittest

from bumblebee.engine import Module
from tests.util import MockWidget

class TestModule(unittest.TestCase):
    def setUp(self):
        self.widget = MockWidget("foo")
        self.moduleWithoutWidgets = Module(engine=None, widgets=None)
        self.moduleWithOneWidget = Module(engine=None, widgets=self.widget)
        self.moduleWithMultipleWidgets = Module(engine=None,
            widgets=[self.widget, self.widget, self.widget]
        )

    def test_empty_widgets(self):
        self.assertEquals(self.moduleWithoutWidgets.widgets(), [])

    def test_single_widget(self):
        self.assertEquals(self.moduleWithOneWidget.widgets(), [self.widget])

    def test_multiple_widgets(self):
        for widget in self.moduleWithMultipleWidgets.widgets():
            self.assertEquals(widget, self.widget)

# pylint: disable=C0103,C0111,W0703

import unittest

from bumblebee.engine import Module
from bumblebee.config import Config
from tests.util import MockWidget

class TestModule(unittest.TestCase):
    def setUp(self):
        self.widget = MockWidget("foo")
        self.config = Config()
        self.moduleWithoutWidgets = Module(engine=None, widgets=None)
        self.moduleWithOneWidget = Module(engine=None, widgets=self.widget)
        self.moduleWithMultipleWidgets = Module(engine=None,
            widgets=[self.widget, self.widget, self.widget]
        )

        self.anyConfigName = "cfg"
        self.anotherConfigName = "cfg2"
        self.anyModule = Module(engine=None, widgets=self.widget, config={
            "name": self.anyConfigName, "config": self.config
        })
        self.anotherModule = Module(engine=None, widgets=self.widget, config={
            "name": self.anotherConfigName, "config": self.config
        })
        self.anyKey = "some-parameter"
        self.anyValue = "value"
        self.anotherValue = "another-value"
        self.emptyKey = "i-do-not-exist"
        self.config.set("{}.{}".format(self.anyConfigName, self.anyKey), self.anyValue)
        self.config.set("{}.{}".format(self.anotherConfigName, self.anyKey), self.anotherValue)

    def test_empty_widgets(self):
        self.assertEquals(self.moduleWithoutWidgets.widgets(), [])

    def test_single_widget(self):
        self.assertEquals(self.moduleWithOneWidget.widgets(), [self.widget])

    def test_multiple_widgets(self):
        for widget in self.moduleWithMultipleWidgets.widgets():
            self.assertEquals(widget, self.widget)

    def test_parameters(self):
        self.assertEquals(self.anyModule.parameter(self.anyKey), self.anyValue)
        self.assertEquals(self.anotherModule.parameter(self.anyKey), self.anotherValue)

    def test_default_parameters(self):
        self.assertEquals(self.anyModule.parameter(self.emptyKey), None)
        self.assertEquals(self.anyModule.parameter(self.emptyKey, self.anyValue), self.anyValue)

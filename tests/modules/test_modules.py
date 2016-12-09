# pylint: disable=C0103,C0111

import unittest
import importlib

from bumblebee.modules.cpu import Module
from bumblebee.engine import modules
from bumblebee.config import Config
from tests.util import assertWidgetAttributes, MockEngine

class TestGenericModules(unittest.TestCase):
    def setUp(self):
        engine = MockEngine()
        config = Config()
        self.objects = {}
        for mod in modules():
            cls = importlib.import_module("bumblebee.modules.{}".format(mod["name"]))
            self.objects[mod["name"]] = getattr(cls, "Module")(engine, { "config": config })

    def test_widgets(self):
        for mod in self.objects:
            widgets = self.objects[mod].widgets()
            for widget in widgets:
                assertWidgetAttributes(self, widget)

    def test_update(self):
        for mod in self.objects:
            widgets = self.objects[mod].widgets()
            self.objects[mod].update(widgets)
            self.test_widgets()
            self.assertEquals(widgets, self.objects[mod].widgets())

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

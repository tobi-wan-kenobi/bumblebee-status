# pylint: disable=C0103,C0111

import mock
import unittest
import importlib

import tests.mocks as mocks

from bumblebee.engine import all_modules
from bumblebee.output import Widget
from bumblebee.config import Config

class TestGenericModules(unittest.TestCase):
    def setUp(self):
        engine = mock.Mock()
        engine.input = mock.Mock()
        config = Config()
        self.objects = {}
        for mod in all_modules():
            cls = importlib.import_module("bumblebee.modules.{}".format(mod["name"]))
            self.objects[mod["name"]] = getattr(cls, "Module")(engine, {"config": config})
            for widget in self.objects[mod["name"]].widgets():
                self.assertEquals(widget.get("variable", None), None)

    def test_widgets(self):
        popen = mocks.MockPopen()
        popen.mock.communicate.return_value = (str.encode("1"), "error")
        popen.mock.returncode = 0

        for mod in self.objects:
            widgets = self.objects[mod].widgets()
            for widget in widgets:
                widget.link_module(self.objects[mod])
                self.assertEquals(widget.module, mod)
                self.assertTrue(isinstance(widget, Widget))
                self.assertTrue(hasattr(widget, "full_text"))
                widget.set("variable", "value")
                self.assertEquals(widget.get("variable", None), "value")
                self.assertTrue(isinstance(widget.full_text(), str) or isinstance(widget.full_text(), unicode))
        popen.cleanup()

    def test_update(self):
        popen = mocks.MockPopen()
        popen.mock.communicate.return_value = (str.encode("1"), "error")
        popen.mock.returncode = 0
        for mod in self.objects:
            widgets = self.objects[mod].widgets()
            self.objects[mod].update(widgets)
            self.test_widgets()
            self.assertEquals(widgets, self.objects[mod].widgets())
        popen.cleanup()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

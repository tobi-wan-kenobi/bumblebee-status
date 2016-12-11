# pylint: disable=C0103,C0111

import unittest
import importlib
import mock

from bumblebee.engine import all_modules
from bumblebee.config import Config
from tests.util import assertWidgetAttributes, MockEngine

class MockCommunicate(object):
    def __init__(self):
        self.returncode = 0

    def communicate(self):
        return (str.encode("1"), "error")

class TestGenericModules(unittest.TestCase):
    @mock.patch("subprocess.Popen")
    def setUp(self, mock_output):
        mock_output.return_value = MockCommunicate()
        engine = MockEngine()
        config = Config()
        self.objects = {}
        for mod in all_modules():
            cls = importlib.import_module("bumblebee.modules.{}".format(mod["name"]))
            self.objects[mod["name"]] = getattr(cls, "Module")(engine, {"config": config})
            for widget in self.objects[mod["name"]].widgets():
                self.assertEquals(widget.get("variable", None), None)

    @mock.patch("subprocess.Popen")
    def test_widgets(self, mock_output):
        mock_output.return_value = MockCommunicate()
        for mod in self.objects:
            widgets = self.objects[mod].widgets()
            for widget in widgets:
                widget.link_module(self.objects[mod])
                self.assertEquals(widget.module, mod)
                assertWidgetAttributes(self, widget)
                widget.set("variable", "value")
                self.assertEquals(widget.get("variable", None), "value")
                self.assertTrue(isinstance(widget.full_text(), str))

    @mock.patch("subprocess.Popen")
    def test_update(self, mock_output):
        mock_output.return_value = MockCommunicate()
        rv = mock.Mock()
        rv.configure_mock(**{
            "communicate.return_value": ("out", None)
        })
        for mod in self.objects:
            widgets = self.objects[mod].widgets()
            self.objects[mod].update(widgets)
            self.test_widgets()
            self.assertEquals(widgets, self.objects[mod].widgets())

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# pylint: disable=C0103,C0111

import sys
import json
import unittest
import mock

from contextlib import contextmanager

import bumblebee.input
from bumblebee.input import I3BarInput
from bumblebee.modules.battery import Module
from tests.util import MockEngine, MockConfig, assertPopen

class MockOpen(object):
    def __init__(self):
        self._value = ""

    def returns(self, value):
        self._value = value

    def __enter__(self):
        return self

    def __exit__(self, a, b, c):
        pass

    def read(self):
        return self._value

class TestBatteryModule(unittest.TestCase):
    def setUp(self):
        self.engine = MockEngine()
        self.config = MockConfig()
        self.module = Module(engine=self.engine, config={ "config": self.config })
        for widget in self.module.widgets():
            widget.link_module(self.module)

    @mock.patch("sys.stdout")
    def test_format(self, mock_output):
        for widget in self.module.widgets():
            self.assertEquals(len(widget.full_text()), len("100%"))

    @mock.patch("os.path.exists")
    @mock.patch("{}.open".format("__builtin__" if sys.version_info[0] < 3 else "builtins"))
    @mock.patch("subprocess.Popen")
    def test_critical(self, mock_output, mock_open, mock_exists):
        mock_open.return_value = MockOpen()
        mock_open.return_value.returns("19")
        mock_exists.return_value = True
        self.config.set("battery.critical", "20")
        self.config.set("battery.warning", "25")
        self.module.update(self.module.widgets())
        self.assertTrue("critical" in self.module.widgets()[0].state())

    @mock.patch("os.path.exists")
    @mock.patch("{}.open".format("__builtin__" if sys.version_info[0] < 3 else "builtins"))
    @mock.patch("subprocess.Popen")
    def test_warning(self, mock_output, mock_open, mock_exists):
        mock_open.return_value = MockOpen()
        mock_exists.return_value = True
        mock_open.return_value.returns("22")
        self.config.set("battery.critical", "20")
        self.config.set("battery.warning", "25")
        self.module.update(self.module.widgets())
        self.assertTrue("warning" in self.module.widgets()[0].state())

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

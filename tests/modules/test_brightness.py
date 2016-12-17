# pylint: disable=C0103,C0111

import json
import unittest
import mock

import bumblebee.input
from bumblebee.input import I3BarInput
from bumblebee.modules.brightness import Module
from tests.util import MockEngine, MockConfig, assertPopen, assertMouseEvent

class TestBrightnessModule(unittest.TestCase):
    def setUp(self):
        self.engine = MockEngine()
        self.engine.input = I3BarInput()
        self.engine.input.need_event = True
        self.config = MockConfig()
        self.module = Module(engine=self.engine, config={ "config": self.config })
        for widget in self.module.widgets():
            widget.link_module(self.module)

    @mock.patch("sys.stdout")
    def test_format(self, mock_output):
        for widget in self.module.widgets():
            self.assertEquals(len(widget.full_text()), len("100%"))

    @mock.patch("select.epoll")
    @mock.patch("subprocess.Popen")
    @mock.patch("sys.stdin")
    def test_wheel_up(self, mock_input, mock_output, mock_select):
        assertMouseEvent(mock_input, mock_output, mock_select, self.engine,
            self.module, bumblebee.input.WHEEL_UP,
            "xbacklight +2%"
        )

    @mock.patch("select.epoll")
    @mock.patch("subprocess.Popen")
    @mock.patch("sys.stdin")
    def test_wheel_down(self, mock_input, mock_output, mock_select):
        assertMouseEvent(mock_input, mock_output, mock_select, self.engine,
            self.module, bumblebee.input.WHEEL_DOWN,
            "xbacklight -2%"
        )

    @mock.patch("select.epoll")
    @mock.patch("subprocess.Popen")
    @mock.patch("sys.stdin")
    def test_custom_step(self, mock_input, mock_output, mock_select):
        self.config.set("brightness.step", "10")
        module = Module(engine=self.engine, config={ "config": self.config })
        assertMouseEvent(mock_input, mock_output, mock_select, self.engine,
            module, bumblebee.input.WHEEL_DOWN,
            "xbacklight -10%"
        )

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

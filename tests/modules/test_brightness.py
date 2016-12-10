# pylint: disable=C0103,C0111

import json
import unittest
import mock

import bumblebee.input
from bumblebee.input import I3BarInput
from bumblebee.modules.brightness import Module
from tests.util import MockEngine, MockConfig, assertPopen

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

    @mock.patch("select.select")
    @mock.patch("subprocess.Popen")
    @mock.patch("sys.stdin")
    def test_wheel_up(self, mock_input, mock_output, mock_select):
        mock_input.readline.return_value = json.dumps({
            "name": self.module.id,
            "button": bumblebee.input.WHEEL_UP,
            "instance": None
        })
        mock_select.return_value = (1,2,3)
        self.engine.input.start()
        self.engine.input.stop()
        mock_input.readline.assert_any_call()
        assertPopen(mock_output, "xbacklight +2%")

    @mock.patch("select.select")
    @mock.patch("subprocess.Popen")
    @mock.patch("sys.stdin")
    def test_wheel_down(self, mock_input, mock_output, mock_select):
        mock_input.readline.return_value = json.dumps({
            "name": self.module.id,
            "button": bumblebee.input.WHEEL_DOWN,
            "instance": None
        })
        mock_select.return_value = (1,2,3)
        self.engine.input.start()
        self.engine.input.stop()
        mock_input.readline.assert_any_call()
        assertPopen(mock_output, "xbacklight -2%")

    @mock.patch("select.select")
    @mock.patch("subprocess.Popen")
    @mock.patch("sys.stdin")
    def test_custom_step(self, mock_input, mock_output, mock_select):
        self.config.set("brightness.step", "10")
        module = Module(engine=self.engine, config={ "config": self.config })
        mock_input.readline.return_value = json.dumps({
            "name": module.id,
            "button": bumblebee.input.WHEEL_DOWN,
            "instance": None
        })
        mock_select.return_value = (1,2,3)
        self.engine.input.start()
        self.engine.input.stop()
        mock_input.readline.assert_any_call()
        assertPopen(mock_output, "xbacklight -10%")

# pylint: disable=C0103,C0111

import unittest
import json
import subprocess
import mock

import bumblebee.input
from bumblebee.input import I3BarInput
from tests.util import MockWidget, MockModule

class TestI3BarInput(unittest.TestCase):
    def setUp(self):
        self.inp = I3BarInput()
        self.inp.need_event = True
        self.anyModule = MockModule()
        self.anyWidget = MockWidget("test")
        self.anyModule.id = "test-module"
        self._called = 0

    def callback(self, event):
        self._called += 1

    @mock.patch("sys.stdin")
    def test_basic_read_event(self, mock_input):
        mock_input.readline.return_value = ""
        self.inp.start()
        self.inp.stop()
        mock_input.readline.assert_any_call()

    @mock.patch("sys.stdin")
    def test_ignore_invalid_data(self, mock_input):
        mock_input.readline.return_value = "garbage"
        self.inp.start()
        self.assertEquals(self.inp.alive(), True)
        self.assertEquals(self.inp.stop(), True)
        mock_input.readline.assert_any_call()

    @mock.patch("sys.stdin")
    def test_ignore_invalid_event(self, mock_input):
        mock_input.readline.return_value = json.dumps({
            "name": None,
            "instance": None,
            "button": None,
        })
        self.inp.start()
        self.assertEquals(self.inp.alive(), True)
        self.assertEquals(self.inp.stop(), True)
        mock_input.readline.assert_any_call()

    @mock.patch("sys.stdin")
    def test_global_callback(self, mock_input):
        mock_input.readline.return_value = json.dumps({
            "name": "somename",
            "instance": "someinstance",
            "button": bumblebee.input.LEFT_MOUSE,
        })
        self.inp.register_callback(None, button=1, cmd=self.callback)
        self.inp.start()
        self.assertEquals(self.inp.stop(), True)
        mock_input.readline.assert_any_call()
        self.assertTrue(self._called > 0)

    @mock.patch("sys.stdin")
    def test_global_callback_button_missmatch(self, mock_input):
        mock_input.readline.return_value = json.dumps({
            "name": "somename",
            "instance": "someinstance",
            "button": bumblebee.input.RIGHT_MOUSE,
        })
        self.inp.register_callback(None, button=1, cmd=self.callback)
        self.inp.start()
        self.assertEquals(self.inp.stop(), True)
        mock_input.readline.assert_any_call()
        self.assertTrue(self._called == 0)

    @mock.patch("sys.stdin")
    def test_module_callback(self, mock_input):
        mock_input.readline.return_value = json.dumps({
            "name": self.anyModule.id,
            "instance": None,
            "button": bumblebee.input.LEFT_MOUSE,
        })
        self.inp.register_callback(self.anyModule, button=1, cmd=self.callback)
        self.inp.start()
        self.assertEquals(self.inp.stop(), True)
        mock_input.readline.assert_any_call()
        self.assertTrue(self._called > 0)

    @mock.patch("sys.stdin")
    def test_widget_callback(self, mock_input):
        mock_input.readline.return_value = json.dumps({
            "name": "test",
            "instance": self.anyWidget.id,
            "button": bumblebee.input.LEFT_MOUSE,
        })
        self.inp.register_callback(self.anyWidget, button=1, cmd=self.callback)
        self.inp.start()
        self.assertEquals(self.inp.stop(), True)
        mock_input.readline.assert_any_call()
        self.assertTrue(self._called > 0)

    @mock.patch("subprocess.Popen")
    @mock.patch("sys.stdin")
    def test_widget_cmd_callback(self, mock_input, mock_output):
        mock_input.readline.return_value = json.dumps({
            "name": "test",
            "instance": self.anyWidget.id,
            "button": bumblebee.input.LEFT_MOUSE,
        })
        self.inp.register_callback(self.anyWidget, button=1, cmd="echo")
        self.inp.start()
        self.assertEquals(self.inp.stop(), True)
        mock_input.readline.assert_any_call()
        mock_output.assert_called_with(["echo"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

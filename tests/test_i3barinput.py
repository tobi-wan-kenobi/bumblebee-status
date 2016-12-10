# pylint: disable=C0103,C0111

import unittest
import json
import subprocess
import mock

import bumblebee.input
from bumblebee.input import I3BarInput
from tests.util import MockWidget, MockModule, assertPopen

class TestI3BarInput(unittest.TestCase):
    def setUp(self):
        self.input = I3BarInput()
        self.input.need_event = True
        self.anyModule = MockModule()
        self.anyWidget = MockWidget("test")
        self.anyModule.id = "test-module"
        self._called = 0

    def callback(self, event):
        self._called += 1

    @mock.patch("sys.stdin")
    def test_basic_read_event(self, mock_input):
        mock_input.readline.return_value = ""
        self.input.start()
        self.input.stop()
        mock_input.readline.assert_any_call()

    @mock.patch("sys.stdin")
    def test_ignore_invalid_data(self, mock_input):
        mock_input.readline.return_value = "garbage"
        self.input.start()
        self.assertEquals(self.input.alive(), True)
        self.assertEquals(self.input.stop(), True)
        mock_input.readline.assert_any_call()

    @mock.patch("sys.stdin")
    def test_ignore_invalid_event(self, mock_input):
        mock_input.readline.return_value = json.dumps({
            "name": None,
            "instance": None,
            "button": None,
        })
        self.input.start()
        self.assertEquals(self.input.alive(), True)
        self.assertEquals(self.input.stop(), True)
        mock_input.readline.assert_any_call()

    @mock.patch("sys.stdin")
    def test_global_callback(self, mock_input):
        mock_input.readline.return_value = json.dumps({
            "name": "somename",
            "instance": "someinstance",
            "button": bumblebee.input.LEFT_MOUSE,
        })
        self.input.register_callback(None, button=1, cmd=self.callback)
        self.input.start()
        self.assertEquals(self.input.stop(), True)
        mock_input.readline.assert_any_call()
        self.assertTrue(self._called > 0)

    @mock.patch("sys.stdin")
    def test_remove_global_callback(self, mock_input):
        mock_input.readline.return_value = json.dumps({
            "name": "somename",
            "instance": "someinstance",
            "button": bumblebee.input.LEFT_MOUSE,
        })
        self.input.register_callback(None, button=1, cmd=self.callback)
        self.input.deregister_callbacks(None)
        self.input.start()
        self.assertEquals(self.input.stop(), True)
        mock_input.readline.assert_any_call()
        self.assertTrue(self._called == 0)

    @mock.patch("sys.stdin")
    def test_global_callback_button_missmatch(self, mock_input):
        mock_input.readline.return_value = json.dumps({
            "name": "somename",
            "instance": "someinstance",
            "button": bumblebee.input.RIGHT_MOUSE,
        })
        self.input.register_callback(None, button=1, cmd=self.callback)
        self.input.start()
        self.assertEquals(self.input.stop(), True)
        mock_input.readline.assert_any_call()
        self.assertTrue(self._called == 0)

    @mock.patch("sys.stdin")
    def test_module_callback(self, mock_input):
        mock_input.readline.return_value = json.dumps({
            "name": self.anyModule.id,
            "instance": None,
            "button": bumblebee.input.LEFT_MOUSE,
        })
        self.input.register_callback(self.anyModule, button=1, cmd=self.callback)
        self.input.start()
        self.assertEquals(self.input.stop(), True)
        mock_input.readline.assert_any_call()
        self.assertTrue(self._called > 0)

    @mock.patch("sys.stdin")
    def test_remove_module_callback(self, mock_input):
        mock_input.readline.return_value = json.dumps({
            "name": self.anyModule.id,
            "instance": None,
            "button": bumblebee.input.LEFT_MOUSE,
        })
        self.input.register_callback(self.anyModule, button=1, cmd=self.callback)
        self.input.deregister_callbacks(self.anyModule)
        self.input.start()
        self.assertEquals(self.input.stop(), True)
        mock_input.readline.assert_any_call()
        self.assertTrue(self._called == 0)

    @mock.patch("sys.stdin")
    def test_widget_callback(self, mock_input):
        mock_input.readline.return_value = json.dumps({
            "name": "test",
            "instance": self.anyWidget.id,
            "button": bumblebee.input.LEFT_MOUSE,
        })
        self.input.register_callback(self.anyWidget, button=1, cmd=self.callback)
        self.input.start()
        self.assertEquals(self.input.stop(), True)
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
        self.input.register_callback(self.anyWidget, button=1, cmd="echo")
        self.input.start()
        self.assertEquals(self.input.stop(), True)
        mock_input.readline.assert_any_call()
        assertPopen(mock_output, "echo")

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

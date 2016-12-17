# pylint: disable=C0103,C0111

import json
import unittest
import mock

import bumblebee.input
from bumblebee.input import I3BarInput
from bumblebee.modules.pulseaudio import Module
from tests.util import MockEngine, MockConfig, assertPopen, assertMouseEvent, assertStateContains

class TestPulseAudioModule(unittest.TestCase):
    def setUp(self):
        self.engine = MockEngine()
        self.engine.input = I3BarInput()
        self.engine.input.need_event = True
        self.config = MockConfig()
        self.module = Module(engine=self.engine, config={ "config": self.config })

    @mock.patch("select.epoll")
    @mock.patch("subprocess.Popen")
    @mock.patch("sys.stdin")
    def test_leftclick(self, mock_input, mock_output, mock_select):
        assertMouseEvent(mock_input, mock_output, mock_select, self.engine,
            self.module, bumblebee.input.LEFT_MOUSE,
            "pactl set-source-mute @DEFAULT_SOURCE@ toggle"
        )

    @mock.patch("select.epoll")
    @mock.patch("subprocess.Popen")
    @mock.patch("sys.stdin")
    def test_rightclick(self, mock_input, mock_output, mock_select):
        assertMouseEvent(mock_input, mock_output, mock_select, self.engine,
            self.module, bumblebee.input.RIGHT_MOUSE,
            "pavucontrol"
        )

    @mock.patch("select.epoll")
    @mock.patch("subprocess.Popen")
    @mock.patch("sys.stdin")
    def test_wheelup(self, mock_input, mock_output, mock_select):
        assertMouseEvent(mock_input, mock_output, mock_select, self.engine,
            self.module, bumblebee.input.WHEEL_UP,
            "pactl set-source-volume @DEFAULT_SOURCE@ +2%"
        )

    @mock.patch("select.epoll")
    @mock.patch("subprocess.Popen")
    @mock.patch("sys.stdin")
    def test_wheeldown(self, mock_input, mock_output, mock_select):
        assertMouseEvent(mock_input, mock_output, mock_select, self.engine,
            self.module, bumblebee.input.WHEEL_DOWN,
            "pactl set-source-volume @DEFAULT_SOURCE@ -2%"
        )

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

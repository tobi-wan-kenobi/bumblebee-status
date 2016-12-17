# pylint: disable=C0103,C0111

import json
import unittest
import mock

import bumblebee.input
from bumblebee.input import I3BarInput
from bumblebee.modules.cpu import Module
from tests.util import MockEngine, MockConfig, assertPopen, assertMouseEvent, assertStateContains

class TestCPUModule(unittest.TestCase):
    def setUp(self):
        self.engine = MockEngine()
        self.engine.input = I3BarInput()
        self.engine.input.need_event = True
        self.config = MockConfig()
        self.module = Module(engine=self.engine, config={ "config": self.config })

    @mock.patch("sys.stdout")
    def test_format(self, mock_output):
        for widget in self.module.widgets():
            self.assertEquals(len(widget.full_text()), len("100.00%"))

    @mock.patch("select.epoll")
    @mock.patch("subprocess.Popen")
    @mock.patch("sys.stdin")
    def test_leftclick(self, mock_input, mock_output, mock_select):
        assertMouseEvent(mock_input, mock_output, mock_select, self.engine,
            self.module, bumblebee.input.LEFT_MOUSE,
            "gnome-system-monitor"
        )

    @mock.patch("psutil.cpu_percent")
    def test_warning(self, mock_psutil):
        self.config.set("cpu.critical", "20")
        self.config.set("cpu.warning", "18")
        mock_psutil.return_value = 19.0
        assertStateContains(self, self.module, "warning")

    @mock.patch("psutil.cpu_percent")
    def test_critical(self, mock_psutil):
        self.config.set("cpu.critical", "20")
        self.config.set("cpu.warning", "19")
        mock_psutil.return_value = 21.0
        assertStateContains(self, self.module, "critical")

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

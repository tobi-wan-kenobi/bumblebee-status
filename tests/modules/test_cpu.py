# pylint: disable=C0103,C0111

import json
import unittest
import mock

import bumblebee.input
from bumblebee.input import I3BarInput
from bumblebee.modules.cpu import Module
from tests.util import MockEngine, MockConfig, assertPopen

class TestCPUModule(unittest.TestCase):
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
            self.assertEquals(len(widget.full_text()), len("100.00%"))

    @mock.patch("subprocess.Popen")
    @mock.patch("sys.stdin")
    def test_leftclick(self, mock_input, mock_output):
        mock_input.readline.return_value = json.dumps({
            "name": self.module.id,
            "button": bumblebee.input.LEFT_MOUSE,
            "instance": None
        })
        self.engine.input.start()
        self.engine.input.stop()
        mock_input.readline.assert_any_call()
        assertPopen(mock_output, "gnome-system-monitor")

    @mock.patch("psutil.cpu_percent")
    def test_warning(self, mock_psutil):
        self.config.set("cpu.critical", "20")
        self.config.set("cpu.warning", "18")
        mock_psutil.return_value = 19.0
        self.module.update(self.module.widgets())
        self.assertEquals(self.module.widgets()[0].state(), "warning")

    @mock.patch("psutil.cpu_percent")
    def test_critical(self, mock_psutil):
        self.config.set("cpu.critical", "20")
        self.config.set("cpu.warning", "19")
        mock_psutil.return_value = 21.0
        self.module.update(self.module.widgets())
        self.assertEquals(self.module.widgets()[0].state(), "critical")

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# pylint: disable=C0103,C0111

import json
import unittest
import mock

import bumblebee.input
from bumblebee.input import I3BarInput
from bumblebee.modules.memory import Module
from tests.util import MockEngine, MockConfig, assertPopen, assertMouseEvent, assertStateContains

class VirtualMemory(object):
    def __init__(self, percent):
        self.percent = percent

class TestMemoryModule(unittest.TestCase):
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
            "gnome-system-monitor"
        )

    @mock.patch("psutil.virtual_memory")
    def test_warning(self, mock_vmem):
        self.config.set("memory.critical", "80")
        self.config.set("memory.warning", "70")
        mock_vmem.return_value = VirtualMemory(75)
        assertStateContains(self, self.module, "warning")

    @mock.patch("psutil.virtual_memory")
    def test_critical(self, mock_vmem):
        self.config.set("memory.critical", "80")
        self.config.set("memory.warning", "70")
        mock_vmem.return_value = VirtualMemory(85)
        assertStateContains(self, self.module, "critical")

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

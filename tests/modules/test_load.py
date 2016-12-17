# pylint: disable=C0103,C0111

import json
import unittest
import mock

import bumblebee.input
from bumblebee.input import I3BarInput
from bumblebee.modules.load import Module
from tests.util import MockEngine, MockConfig, assertStateContains, assertMouseEvent

class TestLoadModule(unittest.TestCase):
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

    @mock.patch("multiprocessing.cpu_count")
    @mock.patch("os.getloadavg")
    def test_warning(self, mock_loadavg, mock_cpucount):
        self.config.set("load.critical", "1")
        self.config.set("load.warning", "0.8")
        mock_cpucount.return_value = 1
        mock_loadavg.return_value = [ 0.9, 0, 0 ]
        assertStateContains(self, self.module, "warning")

    @mock.patch("multiprocessing.cpu_count")
    @mock.patch("os.getloadavg")
    def test_critical(self, mock_loadavg, mock_cpucount):
        self.config.set("load.critical", "1")
        self.config.set("load.warning", "0.8")
        mock_cpucount.return_value = 1
        mock_loadavg.return_value = [ 1.1, 0, 0 ]
        assertStateContains(self, self.module, "critical")

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

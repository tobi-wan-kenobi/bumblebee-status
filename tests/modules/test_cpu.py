# pylint: disable=C0103,C0111

import json
import unittest
import mock

import tests.mocks as mocks

from bumblebee.config import Config
from bumblebee.input import I3BarInput, LEFT_MOUSE
from bumblebee.modules.cpu import Module

class TestCPUModule(unittest.TestCase):
    def setUp(self):
        self._stdin, self._select, self.stdin, self.select = mocks.epoll_mock("bumblebee.input")

        self.popen = mocks.MockPopen()
        self._psutil = mock.patch("bumblebee.modules.cpu.psutil")
        self.psutil = self._psutil.start()

        self.config = Config()
        self.input = I3BarInput()
        self.engine = mock.Mock()
        self.engine.input = self.input
        self.input.need_event = True
        self.module = Module(engine=self.engine, config={ "config": self.config })
        for widget in self.module.widgets():
            widget.link_module(self.module)
            self.anyWidget = widget

    def tearDown(self):
        self._stdin.stop()
        self._select.stop()
        self._psutil.stop()
        self.popen.cleanup()

    def test_format(self):
        self.psutil.cpu_percent.return_value = 21.0
        self.module.update_all()
        for widget in self.module.widgets():
            self.assertEquals(len(widget.full_text()), len("100.00%"))

    def test_leftclick(self):
        mocks.mouseEvent(stdin=self.stdin, button=LEFT_MOUSE, inp=self.input, module=self.module)
        self.popen.assert_call("gnome-system-monitor")

    def test_warning(self):
        self.config.set("cpu.critical", "20")
        self.config.set("cpu.warning", "18")
        self.psutil.cpu_percent.return_value = 19.0
        self.module.update_all()
        self.assertTrue("warning" in self.module.state(self.anyWidget))

    def test_critical(self):
        self.config.set("cpu.critical", "20")
        self.config.set("cpu.warning", "19")
        self.psutil.cpu_percent.return_value = 21.0
        self.module.update_all()
        self.assertTrue("critical" in self.module.state(self.anyWidget))

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

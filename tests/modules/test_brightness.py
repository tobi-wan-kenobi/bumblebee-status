# pylint: disable=C0103,C0111

import mock
import unittest

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import tests.mocks as mocks

from bumblebee.config import Config
from bumblebee.input import I3BarInput, WHEEL_UP, WHEEL_DOWN
from bumblebee.modules.brightness import Module

class TestBrightnessModule(unittest.TestCase):
    def setUp(self):
        self._stdin, self._select, self.stdin, self.select = mocks.epoll_mock("bumblebee.input")

        self.popen = mocks.MockPopen()

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
        self.popen.cleanup()

    def test_format(self):
        for widget in self.module.widgets():
            self.assertEquals(len(widget.full_text()), len("100%"))

    def test_wheel_up(self):
        mocks.mouseEvent(stdin=self.stdin, button=WHEEL_UP, inp=self.input, module=self.module)
        self.popen.assert_call("xbacklight +2%")

    def test_wheel_down(self):
        mocks.mouseEvent(stdin=self.stdin, button=WHEEL_DOWN, inp=self.input, module=self.module)
        self.popen.assert_call("xbacklight -2%")

    def test_custom_step(self):
        self.config.set("brightness.step", "10")
        module = Module(engine=self.engine, config={"config": self.config})
        mocks.mouseEvent(stdin=self.stdin, button=WHEEL_DOWN, inp=self.input, module=module)
        self.popen.assert_call("xbacklight -10%")

    def test_update(self):
        self.popen.mock.communicate.return_value = ("20.0", None)
        self.module.update_all()
        self.assertEquals(self.module.brightness(self.anyWidget), "020%")


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

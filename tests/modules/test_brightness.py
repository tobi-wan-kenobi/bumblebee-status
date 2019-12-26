# pylint: disable=C0103,C0111

import mock
import unittest

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError

import tests.mocks as mocks

import bumblebee.util
from bumblebee.config import Config
from bumblebee.input import WHEEL_UP, WHEEL_DOWN
from bumblebee.modules.brightness import Module

class TestBrightnessModule(unittest.TestCase):
    def setUp(self):
        mocks.setup_test(self, Module)
        self.tool = ""
        self.up = ""
        self.down = ""
        if bumblebee.util.which("light"):
            self.tool = "light"
            self.up = "-A {}%"
            self.down = "-U {}%"
        elif bumblebee.util.which("brightnessctl"):
            self.tool = "brightnessctl"
            self.up = "s {}%+"
            self.down = "s {}%-"
        else:
            self.tool = "xbacklight"
            self.up = "+{}%"
            self.down = "-{}%"

    def tearDown(self):
        mocks.teardown_test(self)

    # def test_format(self):
    #     for widget in self.module.widgets():
    #         self.assertEquals(len(widget.full_text()), len("100%"))

    def test_wheel_up(self):
        mocks.mouseEvent(stdin=self.stdin, button=WHEEL_UP, inp=self.input, module=self.module)
        self.popen.assert_call("{} {}".format(self.tool, self.up.format(2)))

    def test_wheel_down(self):
        mocks.mouseEvent(stdin=self.stdin, button=WHEEL_DOWN, inp=self.input, module=self.module)
        self.popen.assert_call("{} {}".format(self.tool, self.down.format(2)))

    def test_custom_step(self):
        self.config.set("brightness.step", "10")
        module = Module(engine=self.engine, config={"config": self.config})
        mocks.mouseEvent(stdin=self.stdin, button=WHEEL_DOWN, inp=self.input, module=module)
        self.popen.assert_call("{} {}".format(self.tool, self.down.format(10)))

    @mock.patch('bumblebee.modules.brightness.open', create=True)
    def test_error(self,mock_open):
        mock_open.side_effect = FileNotFoundError
        self.module.update_all()
        self.assertEquals(self.module.brightness(self.anyWidget), "n/a")

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

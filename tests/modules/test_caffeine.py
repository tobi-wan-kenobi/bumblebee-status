# pylint: disable=C0103,C0111

import unittest
from mock import patch
import tests.mocks as mocks

from bumblebee.input import LEFT_MOUSE
from bumblebee.modules.caffeine import Module

class TestCaffeineModule(unittest.TestCase):
    def setUp(self):
        mocks.setup_test(self, Module)

    def tearDown(self):
        mocks.teardown_test(self)

    def test_check_requirements(self):
        with patch('bumblebee.util.which', side_effect=['', 'xprop', 'xdg-screensaver']):
            self.assertTrue(['xdotool'] == self.module._check_requirements())

    def test_get_i3bar_xid_returns_digit(self):
        self.popen.mock.communicate.return_value = ("8388614", None)
        self.assertTrue(self.module._get_i3bar_xid().isdigit())

    def test_get_i3bar_xid_returns_error_string(self):
        self.popen.mock.communicate.return_value = ("Some error message", None)
        self.assertTrue(self.module._get_i3bar_xid() is None)

    def test_get_i3bar_xid_returns_empty_string(self):
        self.popen.mock.communicate.return_value = ("", None)
        self.assertTrue(self.module._get_i3bar_xid() is None)

    def test_suspend_screensaver_success(self):
        with patch.object(self.module, '_get_i3bar_xid', return_value=8388614):
            mocks.mouseEvent(stdin=self.stdin, button=LEFT_MOUSE, inp=self.input, module=self.module)
            self.assertTrue(self.module._suspend_screensaver() is True)

    def test_suspend_screensaver_fail(self):
        with patch.object(self.module, '_get_i3bar_xid', return_value=None):
            self.module._active = False
            mocks.mouseEvent(stdin=self.stdin, button=LEFT_MOUSE, inp=self.input, module=self.module)
            self.assertTrue(self.module._suspend_screensaver() is False)

    def test_resume_screensaver(self):
        with patch.object(self.module, '_check_requirements', return_value=[]):
            self.module._active = True
            mocks.mouseEvent(stdin=self.stdin, button=LEFT_MOUSE, inp=self.input, module=self.module)
            self.assertTrue(self.module._resume_screensaver() is True)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# pylint: disable=C0103,C0111

import json
import unittest
import mock

import bumblebee.input
from bumblebee.input import I3BarInput
from bumblebee.modules.cmus import Module
from tests.util import MockEngine, MockConfig, assertPopen

class TestCmusModule(unittest.TestCase):
    def setUp(self):
        self.engine = MockEngine()
        self.module = Module(engine=self.engine, config={"config": MockConfig()})

    @mock.patch("subprocess.Popen")
    def test_read_song(self, mock_output):
        rv = mock.Mock()
        rv.configure_mock(**{
            "communicate.return_value": ("out", None)
        })
        mock_output.return_value = rv
        self.module.update(self.module.widgets())
        assertPopen(mock_output, "cmus-remote -Q")

    def test_widgets(self):
        self.assertTrue(len(self.module.widgets()), 5)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

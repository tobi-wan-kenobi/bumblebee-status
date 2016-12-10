# pylint: disable=C0103,C0111

import json
import unittest
import mock

import bumblebee.input
from bumblebee.input import I3BarInput
from bumblebee.modules.disk import Module
from tests.util import MockEngine, MockConfig, assertPopen

class TestDiskModule(unittest.TestCase):
    def setUp(self):
        self.engine = MockEngine()
        self.engine.input = I3BarInput()
        self.engine.input.need_event = True
        self.config = MockConfig()
        self.config.set("disk.path", "somepath")
        self.module = Module(engine=self.engine, config={"config": self.config})

    @mock.patch("select.select")
    @mock.patch("subprocess.Popen")
    @mock.patch("sys.stdin")
    def test_leftclick(self, mock_input, mock_output, mock_select):
        mock_input.readline.return_value = json.dumps({
            "name": self.module.id,
            "button": bumblebee.input.LEFT_MOUSE,
            "instance": None
        })
        mock_select.return_value = (1,2,3)
        self.engine.input.start()
        self.engine.input.stop()
        mock_input.readline.assert_any_call()
        assertPopen(mock_output, "nautilus {}".format(self.module.parameter("path")))

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

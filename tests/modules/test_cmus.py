# pylint: disable=C0103,C0111

import json
import unittest
import mock

import bumblebee.input
from bumblebee.input import I3BarInput
from bumblebee.modules.cmus import Module
from tests.util import MockEngine, MockConfig, assertPopen, MockEpoll

class TestCmusModule(unittest.TestCase):
    def setUp(self):
        self.engine = MockEngine()
        self.engine.input = I3BarInput()
        self.engine.input.need_event = True
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

    @mock.patch("select.epoll")
    @mock.patch("subprocess.Popen")
    @mock.patch("sys.stdin")
    def test_interaction(self, mock_input, mock_output, mock_select):
        events = [
            {"widget": "cmus.shuffle", "action": "cmus-remote -S"},
            {"widget": "cmus.repeat", "action": "cmus-remote -R"},
            {"widget": "cmus.next", "action": "cmus-remote -n"},
            {"widget": "cmus.prev", "action": "cmus-remote -r"},
            {"widget": "cmus.main", "action": "cmus-remote -u"},
        ]

        mock_input.fileno.return_value = 1
        mock_select.return_value = MockEpoll()

        for event in events:
            mock_input.readline.return_value = json.dumps({
                "name": self.module.id,
                "button": bumblebee.input.LEFT_MOUSE,
                "instance": self.module.widget(event["widget"]).id
            })
            self.engine.input.start()
            self.engine.input.stop()
            mock_input.readline.assert_any_call()
            assertPopen(mock_output, event["action"])

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

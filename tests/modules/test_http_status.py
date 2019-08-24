# pylint: disable=C0103,C0111

import mock
import unittest

from bumblebee.modules.http_status import Module
from bumblebee.config import Config

class TestHttpStatusModule(unittest.TestCase):
    def test_status_success(self):
        config = Config()
        config.set("http_status.target", "http://example.org")
        self.module = Module(engine=mock.Mock(), config={"config":config})

        self.assertTrue(not "warning" in self.module.state(self.module.widgets()[0]))
        self.assertTrue(not "critical" in self.module.state(self.module.widgets()[0]))
        self.assertEqual(self.module.getStatus(), "200")
        self.assertEqual(self.module.getOutput(), "200")

    def test_status_error(self):
        config = Config()
        config.set("http_status.expect", "not a 200")
        config.set("http_status.target", "http://example.org")
        self.module = Module(engine=mock.Mock(), config={"config":config})

        self.assertTrue(not "warning" in self.module.state(self.module.widgets()[0]))
        self.assertTrue("critical" in self.module.state(self.module.widgets()[0]))
        self.assertEqual(self.module.getStatus(), "200")
        self.assertEqual(self.module.getOutput(), "200 != not a 200")

    def test_label(self):
        config = Config()
        config.set("http_status.label", "example")
        config.set("http_status.target", "http://example.org")
        self.module = Module(engine=mock.Mock(), config={"config":config})

        self.assertEqual(self.module.getOutput(), "example: 200")

    def test_unknow(self):
        config = Config()
        config.set("http_status.target", "invalid target")
        self.module = Module(engine=mock.Mock(), config={"config":config})

        self.assertTrue("warning" in self.module.state(self.module.widgets()[0]))
        self.assertEqual(self.module.getStatus(), "UNK")
        self.assertEqual(self.module.getOutput(), "UNK != 200")


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

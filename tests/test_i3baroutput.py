# pylint: disable=C0103,C0111

import json
import unittest
import mock
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from bumblebee.output import I3BarOutput
from tests.util import MockWidget

class TestI3BarOutput(unittest.TestCase):
    def setUp(self):
        self.output = I3BarOutput()
        self.expectedStart = json.dumps({"version": 1, "click_events": True}) + "[\n"
        self.expectedStop = "]\n"
        self.someWidget = MockWidget("foo bar baz")

    @mock.patch("sys.stdout", new_callable=StringIO)
    def test_start(self, stdout):
        self.output.start()
        self.assertEquals(self.expectedStart, stdout.getvalue())

    @mock.patch("sys.stdout", new_callable=StringIO)
    def test_stop(self, stdout):
        self.output.stop()
        self.assertEquals(self.expectedStop, stdout.getvalue())

    @mock.patch("sys.stdout", new_callable=StringIO)
    def test_draw_single_widget(self, stdout):
        self.output.draw(self.someWidget)
        result = json.loads(stdout.getvalue())[0]
        self.assertEquals(result["full_text"], self.someWidget.text())

    @mock.patch("sys.stdout", new_callable=StringIO)
    def test_draw_multiple_widgets(self, stdout):
        self.output.draw([self.someWidget, self.someWidget])
        result = json.loads(stdout.getvalue())
        for res in result:
            self.assertEquals(res["full_text"], self.someWidget.text())

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

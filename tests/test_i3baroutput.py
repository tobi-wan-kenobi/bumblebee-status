# pylint: disable=C0103,C0111
import json
import unittest
import mock
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from bumblebee.output import I3BarOutput

class TestI3BarOutput(unittest.TestCase):
    def setUp(self):
        self.output = I3BarOutput()
        self.expectedStart = json.dumps({"version": 1, "click_events": True}) + "[\n"
        self.expectedStop = "]\n"

    @mock.patch("sys.stdout", new_callable=StringIO)
    def test_start(self, stdout):
        self.output.start()
        self.assertEquals(self.expectedStart, stdout.getvalue())

    @mock.patch("sys.stdout", new_callable=StringIO)
    def test_stop(self, stdout):
        self.output.stop()
        self.assertEquals(self.expectedStop, stdout.getvalue())

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

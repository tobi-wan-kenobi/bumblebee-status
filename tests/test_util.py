# pylint: disable=C0103,C0111

import unittest

from bumblebee.util import *

class TestUtil(unittest.TestCase):
    def test_bytefmt(self):
        value = 10
        display = 10
        units = [ "B", "KiB", "MiB", "GiB" ]
        for unit in units:
            self.assertEquals(bytefmt(value), "{:.2f}{}".format(display, unit))
            value *= 1024
        self.assertEquals(bytefmt(value), "{:.2f}GiB".format(display*1024))

    def test_durationfmt(self):
        self.assertEquals(durationfmt(00), "00:00")
        self.assertEquals(durationfmt(25), "00:25")
        self.assertEquals(durationfmt(60), "01:00")
        self.assertEquals(durationfmt(119), "01:59")
        self.assertEquals(durationfmt(3600), "01:00:00")
        self.assertEquals(durationfmt(7265), "02:01:05")

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

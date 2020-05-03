import unittest

from util.format import *


class format(unittest.TestCase):
    def test_int_from_string(self):
        self.assertEqual(100, asint("100"))
        self.assertEqual(-100, asint("-100"))
        self.assertEqual(0, asint("0"))

    def test_int_from_none(self):
        self.assertEqual(0, asint(None))

    def test_int_from_int(self):
        self.assertEqual(100, asint(100))
        self.assertEqual(-100, asint(-100))
        self.assertEqual(0, asint(0))

    def test_int_minimum(self):
        self.assertEqual(100, asint(100, minimum=10))
        self.assertEqual(100, asint(100, minimum=100))
        self.assertEqual(10, asint(5, minimum=10))

    def test_int_maximum(self):
        self.assertEqual(100, asint(100, maximum=200))
        self.assertEqual(100, asint(100, maximum=100))
        self.assertEqual(100, asint(200, maximum=100))

    def test_true_from_str(self):
        self.assertTrue(asbool("true"))
        self.assertTrue(asbool(True))
        self.assertTrue(asbool("t"))
        self.assertTrue(asbool("1"))
        self.assertTrue(asbool("yes"))
        self.assertTrue(asbool("y"))
        self.assertTrue(asbool("on"))

    def test_false_from_str(self):
        self.assertFalse(asbool("false"))
        self.assertFalse(asbool(False))
        self.assertFalse(asbool("f"))
        self.assertFalse(asbool("0"))
        self.assertFalse(asbool("no"))
        self.assertFalse(asbool("n"))
        self.assertFalse(asbool("off"))
        self.assertFalse(asbool(None))

    def test_list_from_None(self):
        self.assertEqual([], aslist(None))

    def test_list_from_list(self):
        self.assertEqual([1, 2, 3], aslist([1, 2, 3]))

    def test_list_from_str(self):
        self.assertEqual(["12", "13", "14"], aslist("12,13,14"))

    def test_byteformat(self):
        self.assertEqual("500.00B", byte(500))
        self.assertEqual("1.00KiB", byte(1024))
        self.assertEqual("1KiB", byte(1024, "{:.0f}"))
        self.assertEqual("1.50KiB", byte(1024 + 512))
        self.assertEqual("2.50MiB", byte(1024 * 1024 * 2 + 1024 * 512))
        self.assertEqual("4.50GiB", byte(1024 * 1024 * 1024 * 4 + 1024 * 1024 * 512))
        self.assertEqual("2048.00GiB", byte(1024 * 1024 * 1024 * 1024 * 2))

    def test_duration(self):
        self.assertEqual("04:20:00", duration(4 * 60 * 60 + 20 * 60))
        self.assertEqual("04:20:00h", duration(4 * 60 * 60 + 20 * 60, unit=True))
        self.assertEqual(
            "04:20h", duration(4 * 60 * 60 + 20 * 60, compact=True, unit=True)
        )

        self.assertEqual("20:00", duration(20 * 60))
        self.assertEqual("20:00m", duration(20 * 60, unit=True))
        self.assertEqual("20:00m", duration(20 * 60, compact=True, unit=True))

        self.assertEqual("00:20", duration(20))
        self.assertEqual("00:20m", duration(20, unit=True))
        self.assertEqual("00:20m", duration(20, compact=True, unit=True))

        self.assertEqual("n/a", duration(-1))

    def test_seconds(self):
        self.assertEqual(10, seconds(10))
        self.assertEqual(10, seconds("10"))

        self.assertEqual(300, seconds("5m"))
        self.assertEqual(320, seconds("5m20s"))

        self.assertEqual(4 * 3600, seconds("4h"))
        self.assertEqual(4 * 3600 + 5 * 60 + 22, seconds("4h5m22s"))

        self.assertEqual(4 * 3600 + 5 * 60, seconds("4h5m"))

    def test_temperature(self):
        self.assertEqual("10°C", astemperature(10))
        self.assertEqual("10°C", astemperature(10, "metric"))
        self.assertEqual("-100°F", astemperature(-100, "imperial"))
        self.assertEqual("-100°K", astemperature("-100", "kelvin"))


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

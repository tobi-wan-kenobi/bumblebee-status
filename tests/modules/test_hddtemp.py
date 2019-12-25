# -*- coding: utf-8 -*-

import mock
import unittest

from bumblebee.config import Config
import bumblebee.modules.hddtemp


class TestHddtempModule(unittest.TestCase):
    def setUp(self):
        config = Config()
        self.module = bumblebee.modules.hddtemp.Module(
            engine=mock.Mock(), config={"config": config})
        self.data_line = "|/dev/sda|TOSHIBA DT01ACA100                      �|35|C||/dev/sdb|TOSHIBA DT01ACA100                      �|37|C|"
        self.expected_parts = [
            "/dev/sda",
            "TOSHIBA DT01ACA100                      �",
            "35",
            "C",
            "",
            "/dev/sdb",
            "TOSHIBA DT01ACA100                      �",
            "37",
            "C",
            ""]
        self.expected_per_disk = [
            ["/dev/sda",
             "TOSHIBA DT01ACA100                      �",
             "35",
             "C",
             ""],
            ["/dev/sdb",
             "TOSHIBA DT01ACA100                      �",
             "37",
             "C",
             ""]]
        self.device_record = self.expected_per_disk[0]
        self.expected_name_and_temp = ("sda", "35")
        self.expected_hddtemp = "sda+35°C"

    def test_get_parts(self):
        self.assertEqual(
            self.expected_parts, self.module._get_parts(self.data_line))

    def test_partition_parts(self):
        self.assertEqual(
            self.expected_per_disk,
            self.module._partition_parts(self.expected_parts))

    def test_get_name_and_temp(self):
        self.assertEqual(
            self.expected_name_and_temp,
            self.module._get_name_and_temp(self.device_record))

    def test_get_hddtemp(self):
        self.assertEqual(
            self.expected_hddtemp,
            self.module._get_hddtemp(self.expected_name_and_temp))

import unittest
import json
import urllib.request

import util.location


class location(unittest.TestCase):
    def setUp(self):
        patcher = unittest.mock.patch("util.location.urllib.request")
        self.addCleanup(patcher.stop)
        self.request = patcher.start()
        util.location.reset()

        self.primary = {
            "country": "Middle Earth",
            "longitude": "10.0",
            "latitude": "20.5",
            "ip": "127.0.0.1",
        }
        self.secondary = {
            "country_name": "Rivia",
            "longitude": "-10.0",
            "latitude": "-23",
            "ip": "127.0.0.6",
        }

    def test_primary_provider(self):
        self.request.urlopen.return_value.read.return_value = json.dumps(self.primary)
        util.location.country()
        self.assertEqual(self.primary["country"], util.location.country())
        self.assertEqual(
            (self.primary["latitude"], self.primary["longitude"]),
            util.location.coordinates(),
        )
        self.assertEqual(self.primary["ip"], util.location.public_ip())

    def test_secondary_provider(self):
        urlopen = unittest.mock.MagicMock()
        urlopen.read.return_value = json.dumps(self.secondary)
        self.request.urlopen.side_effect = [RuntimeError(), urlopen]

        self.assertEqual(self.secondary["country_name"], util.location.country())
        self.assertEqual(
            (self.secondary["latitude"], self.secondary["longitude"]),
            util.location.coordinates(),
        )
        self.assertEqual(self.secondary["ip"], util.location.public_ip())


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

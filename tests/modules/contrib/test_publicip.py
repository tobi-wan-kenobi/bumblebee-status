import pytest
from unittest import TestCase, mock

import core.config
import core.widget
import modules.contrib.publicip


def build_module():
    config = core.config.Config([])
    return modules.contrib.publicip.Module(config=config, theme=None)

def widget(module):
    return module.widgets()[0]

class PublicIPTest(TestCase):
    def test_load_module(self):
        __import__("modules.contrib.publicip")

    @mock.patch('util.location.location_info')
    def test_public_ip(self, location_mock):
        location_mock.return_value = {
            'public_ip': '5.12.220.2',
            'latitude': 0,
            'longitude': 2,
            'country': 'some country',
            'country_code': 'sc',
            'city_name': '???',
        }

        module = build_module()
        module.update()

        assert widget(module).full_text() == '5.12.220.2 (sc)'

    @mock.patch('util.location.location_info')
    def test_public_ip2(self, location_mock):
        location_mock.return_value = {
            'public_ip': None,
            'latitude': 0,
            'longitude': 2,
            'country': 'some country',
            'country_code': 'sc',
            'city_name': '???',
        }

        module = build_module()
        module.update()

        assert widget(module).full_text() == 'n/a'

    @mock.patch('util.location.location_info')
    def test_public_ip_with_exception(self, location_mock):
        location_mock.side_effect = Exception

        module = build_module()
        module.update()

        assert widget(module).full_text() == 'n/a'

    def test_interval_seconds(self):
        module = build_module()

        assert module.parameter('interval') == 3600

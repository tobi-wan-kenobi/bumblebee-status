import pytest
from unittest import TestCase, mock

import core.config
import core.widget
import modules.contrib.network

def build_module():
    config = core.config.Config([])
    return modules.contrib.network.Module(config=config, theme=None)

def wireless_default():
    return {
        "default": {
            1: ('10.0.1.12', 'wlan0')
        }
    }

def wired_default():
    return {
        'default': {
            18: ('10.0.1.12', 'eth0')
        }
    }

def exec_side_effect(*args, **kwargs):
    if args[0] == "iwgetid":
        return "ESSID: bumblefoo"
    elif "iwconfig" in args[0]:
        return "level=-30"

    return "default"


class TestNetworkUnit(TestCase):
    def test_load_module(self):
        __import__("modules.contrib.network")

    @pytest.mark.allow_hosts(['127.0.0.1'])
    def test_no_internet(self):
        module = build_module()
        assert module.widgets()[0].full_text() == "No connection"

    @mock.patch('util.cli.execute')
    @mock.patch('netifaces.gateways')
    @mock.patch('netifaces.AF_INET', 1)
    def test_wireless_connection(self, gateways_mock, execute_mock):
        fake_ssid = "bumblefoo"
        gateways_mock.return_value = wireless_default()
        execute_mock.side_effect = exec_side_effect

        module = build_module()

        assert fake_ssid in module.widgets()[0].full_text()

    @mock.patch('util.cli.execute')
    @mock.patch('netifaces.gateways')
    @mock.patch('netifaces.AF_INET', 18)
    def test_wired_connection(self, gateways_mock, execute_mock):
        gateways_mock.return_value = wired_default()
        execute_mock.side_effect = exec_side_effect

        module = build_module()

        assert module.widgets()[0].full_text() == "Ethernet"

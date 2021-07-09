from unittest import TestCase, mock
import pytest

import core.config
import core.widget
import modules.contrib.network

import socket

pytest.importorskip("netifaces")


def build_module():
    config = core.config.Config([])
    return modules.contrib.network.Module(config=config, theme=None)


def wireless_default():
    return {"default": {1: ("10.0.1.12", "wlan3")}}


def wired_default():
    return {"default": {18: ("10.0.1.12", "eth3")}}


def exec_side_effect_valid(*args, **kwargs):
    if args[0] == "iwgetid":
        return "ESSID: bumblefoo"
    if "iwconfig" in args[0]:
        return "level=-30"
    return mock.DEFAULT


def exec_side_effect_invalid(*args, **kwargs):
    return "invalid gibberish, can't parse for info"


class TestNetworkUnit(TestCase):
    def test_load_module(self):
        __import__("modules.contrib.network")

    @mock.patch("socket.create_connection")
    def test_no_internet(self, socket_mock):
        socket_mock.side_effect = Exception()
        module = build_module()
        assert module.widgets()[0].full_text() == "No connection"

    @mock.patch("util.cli.execute")
    @mock.patch("netifaces.gateways")
    @mock.patch("socket.create_connection")
    @mock.patch("netifaces.AF_INET", 1)
    @mock.patch("builtins.open", mock.mock_open(read_data="wlan3"))
    def test_valid_wireless_connection(self, socket_mock, gateways_mock, execute_mock):
        socket_mock.return_value = mock.MagicMock()
        fake_ssid = "bumblefoo"
        gateways_mock.return_value = wireless_default()
        execute_mock.side_effect = exec_side_effect_valid

        module = build_module()

        assert fake_ssid in module.widgets()[0].full_text()

    @mock.patch("netifaces.gateways")
    @mock.patch("socket.create_connection")
    @mock.patch("netifaces.AF_INET", 18)
    @mock.patch("builtins.open", mock.mock_open(read_data="wlan3"))
    def test_valid_wired_connection(self, socket_mock, gateways_mock):
        gateways_mock.return_value = wired_default()
        socket_mock.return_value = mock.MagicMock()

        module = build_module()

        assert module.widgets()[0].full_text() == "Ethernet"

    @mock.patch("netifaces.gateways")
    @mock.patch("socket.create_connection")
    def test_invalid_gateways(self, socket_mock, gateways_mock):
        socket_mock.return_value = mock.Mock()
        gateways_mock.return_value = {"xyz": "abc"}

        module = build_module()
        assert module.widgets()[0].full_text() == "No connection"

    @mock.patch("util.cli.execute")
    @mock.patch("socket.create_connection")
    @mock.patch("netifaces.gateways")
    @mock.patch("netifaces.AF_INET", 1)
    @mock.patch("builtins.open", mock.mock_open(read_data="wlan3"))
    def test_invalid_execs(self, gateways_mock, socket_mock, execute_mock):
        execute_mock.side_effect = exec_side_effect_invalid
        socket_mock.return_value = mock.MagicMock()
        gateways_mock.return_value = wireless_default()

        module = build_module()

        assert module.widgets()[0].full_text() == "Unknown ?%"

    @mock.patch("builtins.open", **{"return_value.raiseError.side_effect": Exception()})
    @mock.patch("socket.create_connection")
    @mock.patch("netifaces.gateways")
    @mock.patch("netifaces.AF_INET", 18)
    @mock.patch("builtins.open", mock.mock_open(read_data="wlan3"))
    def test_no_wireless_file(self, gateways_mock, socket_mock, mock_open):
        gateways_mock.return_value = wired_default()
        socket_mock.return_value = mock.MagicMock()
        module = build_module()

        assert module.widgets()[0].full_text() == "Ethernet"

import pytest
from unittest import TestCase, mock

import core.config
import core.widget
import modules.contrib.network_traffic

from types import SimpleNamespace

pytest.importorskip("psutil")
pytest.importorskip("netifaces")

def io_counters_mock(recv, sent):
    return {
        'lo': SimpleNamespace(
            bytes_sent = sent,
            bytes_recv = recv
        )
    }

def gateways_response():
    return {
        'default': {
            1: ('10.0.0.10', 'lo')
        }
    }

def build_module():
    config = core.config.Config([])
    return modules.contrib.network_traffic.Module(config=config, theme=None)

def download_widget(module):
    return module.widgets()[0]

def upload_widget(module):
    return module.widgets()[1]

def mb_to_bytes(value):
    return value*1024**2

class TestNetworkTrafficUnit(TestCase):
    def test_load_module(self):
        __import__("modules.contrib.network_traffic")

    def test_initial_download_rate(self):
        module = build_module()
        assert download_widget(module).full_text() == '0.00B/s'

    def test_initial_upload_rate(self):
        module = build_module()
        assert upload_widget(module).full_text() == '0.00B/s'

    @mock.patch('netifaces.gateways')
    def test_invalid_gateways(self, gateways_mock):
        gateways_mock.return_value = { 'invalid': 'gateways' }

        module = build_module()

        assert download_widget(module).full_text() == '0.00B/s'
        assert upload_widget(module).full_text() == '0.00B/s'

    @mock.patch('psutil.net_io_counters')
    def test_invalid_io_counters(self, net_io_counters_mock):
        net_io_counters_mock.return_value = { 'invalid': 'io_counters' }

        module = build_module()

        assert download_widget(module).full_text() == '0.00B/s'
        assert upload_widget(module).full_text() == '0.00B/s'

    @mock.patch('psutil.net_io_counters')
    @mock.patch('netifaces.gateways')
    @mock.patch('netifaces.AF_INET', 1)
    def test_update_rates(self, gateways_mock, net_io_counters_mock):
        net_io_counters_mock.return_value = io_counters_mock(0, 0)
        gateways_mock.return_value = gateways_response()

        module = build_module()

        assert download_widget(module).full_text() == '0.00B/s'
        assert upload_widget(module).full_text() == '0.00B/s'

        net_io_counters_mock.return_value = io_counters_mock(
            mb_to_bytes(30),
            mb_to_bytes(0.5)
        )

        module.update()

        assert download_widget(module).full_text() == '30.00MiB/s'
        assert upload_widget(module).full_text() == '512.00KiB/s'

    def test_widget_states(self):
        module = build_module()

        assert module.state(download_widget(module)) == 'rx'
        assert module.state(upload_widget(module)) == 'tx'

    def test_invalid_widget_state(self):
        module = build_module()
        invalid_widget = core.widget.Widget(name='invalid')

        assert module.state(invalid_widget) == None

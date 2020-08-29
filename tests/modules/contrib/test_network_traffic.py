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
    return modules.contrib.network_traffic.Module(config=core.config.Config([]), theme=None)

class TestNetworkTrafficUnit(TestCase):
    def test_load_module(self):
        __import__("modules.contrib.network_traffic")

    @mock.patch('psutil.net_io_counters')
    @mock.patch('netifaces.gateways')
    @mock.patch('netifaces.AF_INET', 1)
    def test_update_rates(self, gateways_mock, net_io_counters_mock):
        net_io_counters_mock.return_value = io_counters_mock(0, 0)
        gateways_mock.return_value = gateways_response()

        module = build_module()

        net_io_counters_mock.return_value = io_counters_mock(2842135, 1932215)
        module.update()

        assert module.widgets()[1].full_text() == '1.84MiB/s'
        assert module.widgets()[0].full_text() == '2.71MiB/s'

    def test_initial_download_rate(self):
        module = build_module()
        assert module.widgets()[0].full_text() == '0.00B/s'

    def test_initial_upload_rate(self):
        module = build_module()
        assert module.widgets()[1].full_text() == '0.00B/s'


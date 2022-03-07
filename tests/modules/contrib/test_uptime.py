import pytest
from unittest import TestCase, mock

import core.config
import core.widget
import modules.contrib.uptime


def build_module():
    config = core.config.Config([])
    return modules.contrib.uptime.Module(config=config, theme=None)

def widget(module):
    return module.widgets()[0]

class UptimeTest(TestCase):
    def test_load_module(self):
        __import__("modules.contrib.uptime")

    @mock.patch('builtins.open', new_callable=mock.mock_open, read_data='300000 10.45')
    def test_uptime(self, uptime_mock):
        module = build_module()
        module.update()

        uptime_mock.assert_called_with('/proc/uptime', 'r')
        assert widget(module).full_text() == '3 days, 11:20:00'

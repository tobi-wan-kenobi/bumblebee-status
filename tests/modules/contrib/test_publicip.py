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

    @mock.patch('util.location.public_ip')
    def test_public_ip(self, public_ip_mock):
        public_ip_mock.return_value = '5.12.220.2'

        module = build_module()
        module.update()

        assert widget(module).full_text() == '5.12.220.2'

    @mock.patch('util.location.public_ip')
    def test_public_ip_with_exception(self, public_ip_mock):
        public_ip_mock.side_effect = Exception

        module = build_module()
        module.update()

        assert widget(module).full_text() == 'n/a'

    def test_interval_seconds(self):
        module = build_module()

        assert module.parameter('interval') == 3600

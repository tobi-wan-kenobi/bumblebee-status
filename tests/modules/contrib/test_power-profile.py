from unittest.mock import patch, MagicMock
import unittest
import pytest

import core.config
import modules.contrib.power_profile

pytest.importorskip("dbus")


def build_powerprofile_module():
    config = core.config.Config([])
    return modules.contrib.power_profile.Module(config=config, theme=None)


class TestPowerProfileUnit(unittest.TestCase):
    def __get_mock_dbus_get_method(self, mock_system_bus):
        return (
            mock_system_bus.return_value.get_object.return_value.get_dbus_method.return_value
        )

    def test_load_module(self):
        __import__("modules.contrib.power-profile")

    @patch("dbus.SystemBus")
    def test_full_text(self, mock_system_bus):
        mock_get = self.__get_mock_dbus_get_method(mock_system_bus)
        mock_get.return_value = "balanced"

        module = build_powerprofile_module()
        module.update()
        assert module.widgets()[0].full_text() == "balanced"

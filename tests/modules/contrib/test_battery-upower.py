import pytest

pytest.importorskip("dbus")

def test_load_module():
    __import__("modules.contrib.battery-upower")

def test_load_symbolic_link_module():
    __import__("modules.contrib.battery_upower")


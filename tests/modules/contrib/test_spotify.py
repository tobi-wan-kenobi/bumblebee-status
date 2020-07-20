import pytest

pytest.importorskip("dbus")

def test_load_module():
    __import__("modules.contrib.spotify")


import pytest

pytest.importorskip("power")

def test_load_module():
    __import__("modules.contrib.battery")


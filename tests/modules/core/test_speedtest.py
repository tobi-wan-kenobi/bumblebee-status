import pytest

pytest.importorskip("speedtest")

def test_load_module():
    __import__("modules.core.speedtest")


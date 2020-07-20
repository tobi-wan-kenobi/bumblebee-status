import pytest

pytest.importorskip("datetime")

def test_load_module():
    __import__("modules.contrib.uptime")


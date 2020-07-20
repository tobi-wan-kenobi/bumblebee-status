import pytest

pytest.importorskip("urllib.request")

def test_load_module():
    __import__("modules.contrib.stock")


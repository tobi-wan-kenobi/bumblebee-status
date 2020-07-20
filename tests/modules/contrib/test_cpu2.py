import pytest

pytest.importorskip("psutil")

def test_load_module():
    __import__("modules.contrib.cpu2")


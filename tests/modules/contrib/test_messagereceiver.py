import pytest

pytest.importorskip("socket")

def test_load_module():
    __import__("modules.contrib.messagereceiver")


import pytest

pytest.importorskip("tkinter")

def test_load_module():
    __import__("modules.contrib.bluetooth")


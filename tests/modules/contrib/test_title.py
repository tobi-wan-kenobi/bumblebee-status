import pytest

pytest.importorskip("i3ipc")

def test_load_module():
    __import__("modules.contrib.title")


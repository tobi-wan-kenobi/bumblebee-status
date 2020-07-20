import pytest

pytest.importorskip("subprocess")

def test_load_module():
    __import__("modules.contrib.deadbeef")


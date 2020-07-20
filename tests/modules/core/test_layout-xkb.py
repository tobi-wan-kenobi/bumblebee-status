import pytest

pytest.importorskip("xkbgroup")

def test_load_module():
    __import__("modules.core.layout-xkb")


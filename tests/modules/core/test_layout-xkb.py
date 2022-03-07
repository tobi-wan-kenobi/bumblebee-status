import pytest

pytest.importorskip("xkbgroup")

def test_load_module():
    __import__("modules.core.layout-xkb")

def test_load_symbolic_link_module():
    __import__("modules.core.layout_xkb")

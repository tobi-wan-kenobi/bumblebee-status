import pytest

def test_load_module():
    __import__("modules.contrib.layout-xkbswitch")

def test_load_symbolic_link_module():
    __import__("modules.contrib.layout_xkbswitch")

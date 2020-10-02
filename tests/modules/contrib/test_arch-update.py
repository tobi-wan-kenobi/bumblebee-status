import pytest

def test_load_module():
    __import__("modules.contrib.arch-update")

def test_load_symbolic_link_module():
    __import__("modules.contrib.arch_update")

import pytest

pytest.importorskip("requests")

pytest.importorskip("babel.numbers")

def test_load_module():
    __import__("modules.contrib.currency")


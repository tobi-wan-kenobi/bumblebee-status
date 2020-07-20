import pytest

pytest.importorskip("requests")

def test_load_module():
    __import__("modules.contrib.github")


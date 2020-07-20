import pytest

pytest.importorskip("multiprocessing")

def test_load_module():
    __import__("modules.core.load")


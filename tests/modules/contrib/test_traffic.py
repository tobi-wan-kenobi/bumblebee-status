import pytest

pytest.importorskip("psutil")

pytest.importorskip("netifaces")

def test_load_module():
    __import__("modules.contrib.traffic")


import pytest

pytest.importorskip("netifaces")

pytest.importorskip("subprocess")

def test_load_module():
    __import__("modules.core.nic")


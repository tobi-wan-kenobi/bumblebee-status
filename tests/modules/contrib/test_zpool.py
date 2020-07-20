import pytest

pytest.importorskip("pkg_resources")

def test_load_module():
    __import__("modules.contrib.zpool")


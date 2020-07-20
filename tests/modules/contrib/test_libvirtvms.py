import pytest

pytest.importorskip("libvirt")

def test_load_module():
    __import__("modules.contrib.libvirtvms")


import pytest

pytest.importorskip("yubico")

def test_load_module():
    __import__("modules.contrib.yubikey")


import pytest

pytest.importorskip("requests")

pytest.importorskip("requests.exceptions")

def test_load_module():
    __import__("modules.contrib.getcrypto")


import pytest

pytest.importorskip("requests")

pytest.importorskip("psutil")

def test_load_module():
    __import__("modules.contrib.http_status")


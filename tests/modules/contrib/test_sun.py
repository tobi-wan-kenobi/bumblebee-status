import pytest

pytest.importorskip("suntime")

pytest.importorskip("requests")

pytest.importorskip("dateutil.tz")

pytest.importorskip("datetime")

def test_load_module():
    __import__("modules.contrib.sun")


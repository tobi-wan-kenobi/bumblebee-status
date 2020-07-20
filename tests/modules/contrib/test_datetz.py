import pytest

pytest.importorskip("datetime")

pytest.importorskip("pytz")

pytest.importorskip("tzlocal")

def test_load_module():
    __import__("modules.contrib.datetz")


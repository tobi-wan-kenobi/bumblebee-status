import pytest

pytest.importorskip("tkinter")

pytest.importorskip("PIL")

pytest.importorskip("requests")

pytest.importorskip("simplejson")

def test_load_module():
    __import__("modules.contrib.octoprint")


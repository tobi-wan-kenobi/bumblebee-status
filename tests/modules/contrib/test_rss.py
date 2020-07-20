import pytest

pytest.importorskip("feedparser")

pytest.importorskip("webbrowser")

pytest.importorskip("tempfile")

pytest.importorskip("random")

def test_load_module():
    __import__("modules.contrib.rss")


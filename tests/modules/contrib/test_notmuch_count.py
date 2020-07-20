import pytest

def test_load_module():
    __import__("modules.contrib.notmuch_count")


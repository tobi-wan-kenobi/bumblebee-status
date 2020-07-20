import pytest

pytest.importorskip("datetime")

pytest.importorskip("math")

def test_load_module():
    __import__("modules.contrib.pomodoro")


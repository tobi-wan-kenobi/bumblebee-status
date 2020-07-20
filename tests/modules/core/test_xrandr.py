import pytest

pytest.importorskip("bumblebee_status.discover")

pytest.importorskip("i3")

def test_load_module():
    __import__("modules.core.xrandr")


import pytest

pytest.importorskip("bumblebee_status.discover")

def test_load_module():
    __import__("modules.contrib.pacman")


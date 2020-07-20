import pytest

pytest.importorskip("taskw")

def test_load_module():
    __import__("modules.contrib.taskwarrior")


import pytest

pytest.importorskip("pygit2")

def test_load_module():
    __import__("modules.core.git")


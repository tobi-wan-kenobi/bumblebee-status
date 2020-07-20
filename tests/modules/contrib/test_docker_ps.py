import pytest

pytest.importorskip("docker")

pytest.importorskip("requests.exceptions")

def test_load_module():
    __import__("modules.contrib.docker_ps")


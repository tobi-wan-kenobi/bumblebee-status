import pytest

def test_load_module():
    __import__("modules.contrib.portage_status")


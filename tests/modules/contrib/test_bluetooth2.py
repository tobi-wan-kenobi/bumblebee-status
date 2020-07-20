import pytest

pytest.importorskip("subprocess")

pytest.importorskip("dbus")

pytest.importorskip("dbus.mainloop.glib")

def test_load_module():
    __import__("modules.contrib.bluetooth2")


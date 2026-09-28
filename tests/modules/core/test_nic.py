import pytest

pytest.importorskip("netifaces")

pytest.importorskip("subprocess")

def test_load_module():
    __import__("modules.core.nic")


import io
from unittest import mock

import core.config
import modules.core.nic

PROC_NET_WIRELESS = """Inter-| sta-|   Quality        |   Discarded packets               | Missed | WE
 face | tus | link level noise |  nwid  crypt   frag  retry   misc | beacon | 22
wlan0: 0000   54.  -56.  -256        0      0      0      0      0        0
"""

IW_LINK = """Connected to 00:11:22:33:44:55 (on wlan0)
	SSID: example
	freq: 5180
	signal: -61 dBm
"""


@pytest.fixture
def nic():
    with mock.patch.object(modules.core.nic.Module, "_update_widgets"):
        module = modules.core.nic.Module(core.config.Config([]), theme=None)
    module.iw = "/usr/bin/iw"
    module._iswlan = lambda intf: True
    module._istunnel = lambda intf: False
    return module


def test_strength_from_proc(nic):
    with mock.patch("builtins.open", return_value=io.StringIO(PROC_NET_WIRELESS)), \
         mock.patch("util.cli.execute") as execute:
        assert nic.get_strength_dbm("wlan0") == -56
    execute.assert_not_called()


def test_strength_falls_back_to_iw_without_proc(nic):
    with mock.patch("builtins.open", side_effect=FileNotFoundError), \
         mock.patch("util.cli.execute", return_value=IW_LINK):
        assert nic.get_strength_dbm("wlan0") == -61


def test_strength_falls_back_to_iw_when_intf_not_in_proc(nic):
    with mock.patch("builtins.open", return_value=io.StringIO(PROC_NET_WIRELESS)), \
         mock.patch("util.cli.execute", return_value=IW_LINK):
        assert nic.get_strength_dbm("wlan1") == -61


def test_strength_none_when_iw_fails(nic):
    with mock.patch("builtins.open", side_effect=FileNotFoundError), \
         mock.patch("util.cli.execute", side_effect=RuntimeError("exited with code 254")):
        assert nic.get_strength_dbm("wlan0") is None


def test_strength_none_without_iw(nic):
    nic.iw = None
    with mock.patch("builtins.open", side_effect=FileNotFoundError):
        assert nic.get_strength_dbm("wlan0") is None

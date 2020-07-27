import sys

from core.input import trigger, LEFT_MOUSE, RIGHT_MOUSE
from core.config import Config
from modules.core.xrandr import Module


MOCK_EXECUTE = "modules.core.xrandr.util.cli.execute"


def mock_xrandr(mocker, xrandr_output):
    return mocker.patch(MOCK_EXECUTE, return_value=xrandr_output)


def assert_widgets(module, *expected_widgets):
    assert len(module.widgets()) == len(expected_widgets)

    for widget, (name, state, pos) in zip(module.widgets(), expected_widgets):
        assert widget.name == name
        assert widget.get("state") == state
        assert widget.get("pos") == pos


def assert_trigger(xrandr_cli, module, widget_index, button, expected_command):
    xrandr_cli.reset_mock()

    widget = module.widgets()[widget_index]
    trigger({"button": button, "instance": widget.id, "name": module.id})

    if expected_command is None:
        xrandr_cli.assert_called_once_with("xrandr -q")
    else:
        assert xrandr_cli.call_count == 2
        xrandr_cli.assert_any_call(expected_command)
        xrandr_cli.assert_called_with("xrandr -q")


def test_autoupdate(mocker):
    xrandr_cli = mock_xrandr(mocker, HDMI_CONNECTED_ACTIVE)
    module = Module(Config([]), theme=None)
    module.update()
    xrandr_cli.assert_called_once_with("xrandr -q")

    assert_widgets(module, ("eDP-1-1", "on", 0), ("HDMI-1-1", "on", 1920))

    assert_trigger(xrandr_cli, module, 0, LEFT_MOUSE, "xrandr --output eDP-1-1 --off")
    assert_trigger(xrandr_cli, module, 0, RIGHT_MOUSE, "xrandr --output eDP-1-1 --off")
    assert_trigger(xrandr_cli, module, 1, LEFT_MOUSE, "xrandr --output HDMI-1-1 --off")
    assert_trigger(xrandr_cli, module, 1, RIGHT_MOUSE, "xrandr --output HDMI-1-1 --off")


def test_display_off(mocker):
    xrandr_cli = mock_xrandr(mocker, HDMI_CONNECTED_INACTIVE)
    module = Module(Config([]), theme=None)
    module.update()
    xrandr_cli.assert_called_once_with("xrandr -q")

    assert_widgets(module, ("eDP-1-1", "on", 0), ("HDMI-1-1", "off", sys.maxsize))

    assert_trigger(xrandr_cli, module, 0, LEFT_MOUSE, None)
    assert_trigger(xrandr_cli, module, 0, RIGHT_MOUSE, None)
    assert_trigger(xrandr_cli, module, 1, LEFT_MOUSE, "xrandr --output HDMI-1-1 --auto --left-of eDP-1-1")
    assert_trigger(xrandr_cli, module, 1, RIGHT_MOUSE, "xrandr --output HDMI-1-1 --auto --right-of eDP-1-1")


def test_no_autoupdate(mocker):
    xrandr_cli = mock_xrandr(mocker, HDMI_CONNECTED_ACTIVE)
    module = Module(Config(["-p", "xrandr.autoupdate=false"]), theme=None)
    module.update()
    xrandr_cli.assert_called_once_with("xrandr -q")

    assert_widgets(
        module, ("eDP-1-1", "on", 0), ("HDMI-1-1", "on", 1920), (None, "refresh", None)
    )

    assert_trigger(xrandr_cli, module, 0, LEFT_MOUSE, "xrandr --output eDP-1-1 --off")
    assert_trigger(xrandr_cli, module, 0, RIGHT_MOUSE, "xrandr --output eDP-1-1 --off")
    assert_trigger(xrandr_cli, module, 1, LEFT_MOUSE, "xrandr --output HDMI-1-1 --off")
    assert_trigger(xrandr_cli, module, 1, RIGHT_MOUSE, "xrandr --output HDMI-1-1 --off")


def test_exclude(mocker):
    xrandr_cli = mock_xrandr(mocker, HDMI_CONNECTED_ACTIVE)
    module = Module(Config(["-p", "xrandr.exclude=eDP"]), theme=None)
    module.update()
    xrandr_cli.assert_called_once_with("xrandr -q")

    assert_widgets(module, ("HDMI-1-1", "on", 1920))

    assert_trigger(xrandr_cli, module, 0, LEFT_MOUSE, "xrandr --output HDMI-1-1 --off")
    assert_trigger(xrandr_cli, module, 0, RIGHT_MOUSE, "xrandr --output HDMI-1-1 --off")


def test_exclude_off(mocker):
    xrandr_cli = mock_xrandr(mocker, HDMI_CONNECTED_INACTIVE)
    module = Module(Config(["-p", "xrandr.exclude=eDP"]), theme=None)
    module.update()
    xrandr_cli.assert_called_once_with("xrandr -q")

    assert_widgets(module, ("HDMI-1-1", "off", sys.maxsize))

    assert_trigger(xrandr_cli, module, 0, LEFT_MOUSE, "xrandr --output HDMI-1-1 --auto --left-of eDP-1-1")
    assert_trigger(xrandr_cli, module, 0, RIGHT_MOUSE, "xrandr --output HDMI-1-1 --auto --right-of eDP-1-1")


def test_no_autotoggle_inactive_connected(mocker):
    xrandr_cli = mock_xrandr(mocker, HDMI_DISCONNECTED_INACTIVE)
    module = Module(Config([]), theme=None)
    module.update()
    xrandr_cli.assert_called_once_with("xrandr -q")

    assert_widgets(module, ("eDP-1-1", "on", 0))

    xrandr_cli.return_value = HDMI_CONNECTED_INACTIVE
    xrandr_cli.reset_mock()

    module.update()
    xrandr_cli.assert_called_once_with("xrandr -q")


def test_no_autotoggle_active_disconnected(mocker):
    xrandr_cli = mock_xrandr(mocker, HDMI_CONNECTED_ACTIVE)
    module = Module(Config([]), theme=None)
    module.update()
    xrandr_cli.assert_called_once_with("xrandr -q")

    assert_widgets(module, ("eDP-1-1", "on", 0), ("HDMI-1-1", "on", 1920))

    xrandr_cli.return_value = HDMI_DISCONNECTED_ACTIVE
    xrandr_cli.reset_mock()

    module.update()
    xrandr_cli.assert_called_once_with("xrandr -q")


def test_autotoggle_excluded_inactive_connected(mocker):
    xrandr_cli = mock_xrandr(mocker, HDMI_DISCONNECTED_INACTIVE)
    module = Module(Config(["-p", "xrandr.autotoggle=true", "xrandr.exclude=HDMI"]), theme=None)
    module.update()
    xrandr_cli.assert_called_once_with("xrandr -q")

    assert_widgets(module, ("eDP-1-1", "on", 0))

    xrandr_cli.return_value = HDMI_CONNECTED_INACTIVE
    xrandr_cli.reset_mock()

    module.update()
    xrandr_cli.assert_called_once_with("xrandr -q")


def test_autotoggle_excluded_active_disconnected(mocker):
    xrandr_cli = mock_xrandr(mocker, HDMI_CONNECTED_ACTIVE)
    module = Module(Config(["-p", "xrandr.autotoggle=true", "xrandr.exclude=HDMI"]), theme=None)
    module.update()
    xrandr_cli.assert_called_once_with("xrandr -q")

    assert_widgets(module, ("eDP-1-1", "on", 0))

    xrandr_cli.return_value = HDMI_DISCONNECTED_ACTIVE
    xrandr_cli.reset_mock()

    module.update()
    xrandr_cli.assert_called_once_with("xrandr -q")


def test_autotoggle_active_disconnected(mocker):
    xrandr_cli = mock_xrandr(mocker, HDMI_CONNECTED_ACTIVE)
    module = Module(Config(["-p", "xrandr.autotoggle=true"]), theme=None)
    module.update()
    xrandr_cli.assert_called_once_with("xrandr -q")

    assert_widgets(module, ("eDP-1-1", "on", 0), ("HDMI-1-1", "on", 1920))

    xrandr_cli.return_value = HDMI_DISCONNECTED_ACTIVE
    xrandr_cli.reset_mock()

    module.update()
    assert xrandr_cli.call_count == 2
    xrandr_cli.assert_any_call("xrandr -q")
    xrandr_cli.assert_called_with("xrandr --output HDMI-1-1 --off")


def test_autotoggle_inactive_disconnected(mocker):
    xrandr_cli = mock_xrandr(mocker, HDMI_CONNECTED_INACTIVE)
    module = Module(Config(["-p", "xrandr.autotoggle=true"]), theme=None)
    module.update()
    xrandr_cli.assert_called_once_with("xrandr -q")

    assert_widgets(module, ("eDP-1-1", "on", 0), ("HDMI-1-1", "off", sys.maxsize))

    xrandr_cli.return_value = HDMI_DISCONNECTED_INACTIVE
    xrandr_cli.reset_mock()

    module.update()
    xrandr_cli.assert_called_once_with("xrandr -q")


def test_autotoggle_active_connected(mocker):
    xrandr_cli = mock_xrandr(mocker, HDMI_DISCONNECTED_ACTIVE)
    module = Module(Config(["-p", "xrandr.autotoggle=true"]), theme=None)
    module.update()
    xrandr_cli.assert_called_once_with("xrandr -q")

    assert_widgets(module, ("eDP-1-1", "on", 0))

    xrandr_cli.return_value = HDMI_CONNECTED_ACTIVE
    xrandr_cli.reset_mock()

    module.update()
    xrandr_cli.assert_called_once_with("xrandr -q")


def test_autotoggle_inactive_connected(mocker):
    xrandr_cli = mock_xrandr(mocker, HDMI_DISCONNECTED_INACTIVE)
    module = Module(Config(["-p", "xrandr.autotoggle=true"]), theme=None)
    module.update()
    xrandr_cli.assert_called_once_with("xrandr -q")

    assert_widgets(module, ("eDP-1-1", "on", 0))

    xrandr_cli.return_value = HDMI_CONNECTED_INACTIVE
    xrandr_cli.reset_mock()

    module.update()
    assert xrandr_cli.call_count == 2
    xrandr_cli.assert_any_call("xrandr -q")
    xrandr_cli.assert_called_with("xrandr --output HDMI-1-1 --auto --right-of eDP-1-1")


def test_autotoggle_left(mocker):
    xrandr_cli = mock_xrandr(mocker, HDMI_DISCONNECTED_INACTIVE)
    module = Module(Config(["-p", "xrandr.autotoggle=true", "xrandr.autotoggle_side=left"]), theme=None)
    module.update()
    xrandr_cli.assert_called_once_with("xrandr -q")

    assert_widgets(module, ("eDP-1-1", "on", 0))

    xrandr_cli.return_value = HDMI_CONNECTED_INACTIVE
    xrandr_cli.reset_mock()

    module.update()
    assert xrandr_cli.call_count == 2
    xrandr_cli.assert_any_call("xrandr -q")
    xrandr_cli.assert_called_with("xrandr --output HDMI-1-1 --auto --left-of eDP-1-1")


# xrandr sample data

HDMI_CONNECTED_ACTIVE = """
Screen 0: minimum 8 x 8, current 4480 x 1440, maximum 32767 x 32767
eDP-1-1 connected primary 1920x1080+0+0 344mm x 193mm
   1920x1080     60.00*+  59.93    48.00
   1680x1050     59.95    59.88
   1600x1024     60.17
   1400x1050     59.98
   1280x1024     60.02
   1440x900      59.89
   1280x960      60.00
   1360x768      59.80    59.96
   1152x864      60.00
   1024x768      60.04    60.00
   960x720       60.00
   928x696       60.05
   896x672       60.01
   960x600       60.00
   960x540       59.99
   800x600       60.00    60.32    56.25
   840x525       60.01    59.88
   800x512       60.17
   700x525       59.98
   640x512       60.02
   720x450       59.89
   640x480       60.00    59.94
   680x384       59.80    59.96
   576x432       60.06
   512x384       60.00
   400x300       60.32    56.34
   320x240       60.05
HDMI-1-1 connected 2560x1440+1920+0 596mm x 335mm
   2560x1440     59.95*+
   1920x1080     60.00    50.00    59.94
   1920x1080i    60.00    50.00    59.94
   1680x1050     59.88
   1600x900      60.00
   1280x1024     60.02
   1280x800      59.91
   1280x720      60.00    50.00    59.94
   1024x768      60.00
   800x600       60.32
   720x576       50.00
   720x576i      50.00
   720x480       60.00    59.94
   720x480i      60.00    59.94
   640x480       60.00    59.94
"""


HDMI_CONNECTED_INACTIVE = """
eDP-1-1 connected primary 1920x1080+0+0 344mm x 193mm
   1920x1080     60.00*+  59.93    48.00
HDMI-1-1 connected
   2560x1440     59.95 +
"""

HDMI_DISCONNECTED_ACTIVE = """
eDP-1-1 connected primary 1920x1080+0+0 344mm x 193mm
   1920x1080     60.00*+  59.93    48.00
HDMI-1-1 disconnected 2560x1440+1920+0 0mm x 0mm
  2560x1440 (0x6b) 241.500MHz +HSync +VSync
        h: width  2560 start 2608 end 2640 total 2720 skew    0 clock  88.79KHz
        v: height 1440 start 1442 end 1447 total 1481           clock  59.95Hz
"""

HDMI_DISCONNECTED_INACTIVE = """
eDP-1-1 connected primary 1920x1080+0+0 344mm x 193mm
   1920x1080     60.00*+  59.93    48.00
HDMI-1-1 disconnected
"""

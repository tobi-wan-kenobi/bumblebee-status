import pytest

import util.cli
import core.config
import modules.contrib.dunstctl

def build_module():
    return modules.contrib.dunstctl.Module(
        config=core.config.Config([]),
        theme=None
    )

def test_load_module():
    __import__("modules.contrib.dunstctl")

def test_dunst_running(mocker):
    command = mocker.patch('util.cli.execute', return_value=(0, "false"))

    module = build_module()
    module.update()
    widget = module.widget()

    actual = module.state(widget)
    command.assert_called_with('dunstctl is-paused', return_exitcode=True, ignore_errors=True)
    assert actual == ['unmuted']

def test_dunst_paused(mocker):
    command = mocker.patch('util.cli.execute', return_value=(0, "true"))

    module = build_module()
    module.update()
    widget = module.widget()

    actual = module.state(widget)
    command.assert_called_with('dunstctl is-paused', return_exitcode=True, ignore_errors=True)
    assert actual == ['muted', 'warning']

def test_dunst_off(mocker):
    command = mocker.patch('util.cli.execute', return_value=(1, "dontcare"))

    module = build_module()
    module.update()
    widget = module.widget()

    actual = module.state(widget)
    command.assert_called_with('dunstctl is-paused', return_exitcode=True, ignore_errors=True)
    assert actual == ['unknown', 'critical']

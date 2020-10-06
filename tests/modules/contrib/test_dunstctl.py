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
    command = mocker.patch('util.cli.execute', return_value='false')

    module = build_module()
    module.update()

    command.assert_called_with('dunstctl is-paused')

    widget = module.widget()
    assert module.state(widget) == ['unmuted']

def test_dunst_paused(mocker):
    command = mocker.patch('util.cli.execute', return_value='true')

    module = build_module()
    module.update()

    command.assert_called_with('dunstctl is-paused')

    widget = module.widget()
    assert module.state(widget) == ['muted', 'warning']

def test_toggle_status_pause(mocker):
    command = mocker.patch('util.cli.execute')
    command.side_effect = ['true', 'true', None]

    module = build_module()
    module.toggle_status(False)

    command.assert_any_call('dunstctl set-paused false')

def test_toggle_status_unpause(mocker):
    command = mocker.patch('util.cli.execute')
    command.side_effect = ['false', 'false', None]

    module = build_module()
    module.toggle_status(False)

    command.assert_called_with('dunstctl set-paused true')

def test_input_register(mocker):
    command = mocker.patch('util.cli.execute')
    input_register = mocker.patch('core.input.register')

    module = build_module()

    input_register.assert_called_with(
        module,
        button=core.input.LEFT_MOUSE,
        cmd=module.toggle_status
    )


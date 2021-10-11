import pytest

import core.config
import modules.contrib.dunst


def build_module():
    return modules.contrib.dunst.Module(
        config=core.config.Config([]),
        theme=None
    )


def test_load_module():
    __import__("modules.contrib.dunst")

def test_input_registration(mocker):
   input_register = mocker.patch('core.input.register')

   module = build_module()

   input_register.assert_called_with(
       module,
       button=core.input.LEFT_MOUSE,
       cmd=module.toggle_status
   )

def test_dunst_toggle(mocker):
    start_command = mocker.patch('util.cli.execute')

    module = build_module()
    start_command.assert_called_with('killall -s SIGUSR2 dunst', ignore_errors=True)

    toggle_command = mocker.patch('util.cli.execute')
    module.toggle_status(None)
    toggle_command.assert_called_with('killall -s SIGUSR1 dunst')

    widget = module.widget()
    actual = module.state(widget)
    assert actual == ['muted', 'warning']

    module.toggle_status(None)
    toggle_command.assert_called_with('killall -s SIGUSR2 dunst')

    widget = module.widget()
    actual = module.state(widget)
    assert actual == ['unmuted']

def test_dunst_toggle_exception(mocker):
    module = build_module()

    toggle_command = mocker.patch('util.cli.execute', side_effect=Exception)
    module.toggle_status(None)
    toggle_command.assert_called_with('killall -s SIGUSR1 dunst')

    widget = module.widget()
    actual = module.state(widget)
    assert actual == ['unmuted']

import pytest

import util.cli
import core.config
import modules.contrib.layout_xkbswitch

def build_module():
    return modules.contrib.layout_xkbswitch.Module(
        config=core.config.Config([]),
        theme=None
    )

def test_load_module():
    __import__("modules.contrib.layout-xkbswitch")

def test_load_symbolic_link_module():
    __import__("modules.contrib.layout_xkbswitch")

def test_current_layout(mocker):
    command = mocker.patch('util.cli.execute')
    command.side_effect = ['en', 'en']

    module = build_module()
    widget = module.widget()

    module.update()

    assert widget.full_text() == 'en'

def test_current_layout_exception(mocker):
    command = mocker.patch('util.cli.execute')
    command.side_effect = RuntimeError

    module = build_module()
    widget = module.widget()

    module.update()

    assert widget.full_text() == ['n/a']

def test_input_register(mocker):
    input_register = mocker.patch('core.input.register')

    module = build_module()

    input_register.assert_called_with(
        module,
        button=core.input.LEFT_MOUSE,
        cmd=module.next_keymap
    )

def test_next_keymap(mocker):
    command = mocker.patch('util.cli.execute')

    module = build_module()
    module.next_keymap(False)

    command.assert_called_with('xkb-switch -n', ignore_errors=True)

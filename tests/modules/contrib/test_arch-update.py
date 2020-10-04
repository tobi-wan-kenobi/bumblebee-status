import pytest

import util.cli
import core.config
import modules.contrib.arch_update

@pytest.fixture
def module():
    module = modules.contrib.arch_update.Module(
        config=core.config.Config([]),
        theme=None
    )

    yield module

def test_load_module():
    __import__("modules.contrib.arch-update")

def test_load_symbolic_link_module():
    __import__("modules.contrib.arch_update")

def test_with_one_package(module, mocker):
    command = mocker.patch(
        'util.cli.execute',
        return_value=(0, 'bumblebee 1.0.0')
    )

    module.update()

    command.assert_called_with(
        'checkupdates',
        ignore_errors=True,
        return_exitcode=True
    )

    widget = module.widget()
    assert widget.full_text() == 'Update Arch: 1'
    assert module.state(widget) == None
    assert module.hidden() == False

def test_with_two_packages(module, mocker):
    command = mocker.patch(
        'util.cli.execute',
        return_value=(0, 'bumblebee 1.0.0\ni3wm 3.5.7')
    )

    module.update()

    widget = module.widget()
    assert widget.full_text() == 'Update Arch: 2'
    assert module.state(widget) == 'warning'
    assert module.hidden() == False

def test_with_no_packages(module, mocker):
    mocker.patch('util.cli.execute', return_value=(2, ''))

    module.update()

    widget = module.widget()
    assert widget.full_text() == 'Update Arch: 0'
    assert module.state(widget) == None
    assert module.hidden() == True

def test_with_unknown_code(module, mocker):
    mocker.patch('util.cli.execute', return_value=(99, 'error'))
    logger = mocker.patch('logging.error')

    module.update()

    logger.assert_called_with('checkupdates exited with {}: {}'.format(99, 'error'))

    widget = module.widget()
    assert widget.full_text() == 'Update Arch: 0'
    assert module.state(widget) == 'warning'
    assert module.hidden() == False


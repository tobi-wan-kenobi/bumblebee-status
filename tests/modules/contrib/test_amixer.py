import pytest

import util.cli
import core.config
import modules.contrib.amixer

@pytest.fixture
def module_mock(request):
    def _module_mock(config = []):
        return modules.contrib.amixer.Module(
            config=core.config.Config(config),
            theme=None
        )

    yield _module_mock

@pytest.fixture
def amixer_mock():
    def _mock(device='Master', volume='10%', state='on'):
        return """
        Simple mixer control '{device}',0
          Capabilities: pvolume pswitch pswitch-joined
          Playback channels: Front Left - Front Right
          Limits: Playback 0 - 65536
          Mono:
          Front Left: Playback 55705 [{volume}%] [{state}]
          Front Right: Playback 55705 [{volume}%] [{state}]
        """.format(
            device=device,
            volume=volume,
            state=state
        )

    return _mock

def test_load_module():
    __import__("modules.contrib.amixer")

def test_initial_full_text(module_mock, amixer_mock, mocker):
    module = module_mock()
    assert module.widget().full_text() == 'n/a'

def test_input_registration(mocker):
   input_register = mocker.patch('core.input.register')

   module = modules.contrib.amixer.Module(
       config=core.config.Config([]),
       theme=None
   )

   input_register.assert_any_call(
       module,
       button=core.input.WHEEL_DOWN,
       cmd=module.decrease_volume
   )

   input_register.assert_any_call(
       module,
       button=core.input.WHEEL_UP,
       cmd=module.increase_volume
   )

   input_register.assert_any_call(
       module,
       button=core.input.LEFT_MOUSE,
       cmd=module.toggle
   )

def test_volume_update(module_mock, amixer_mock, mocker):
    mocker.patch(
        'util.cli.execute',
        return_value=amixer_mock(volume='25%', state='on')
    )

    module = module_mock()
    widget = module.widget()

    module.update()
    assert widget.full_text() == '25%'
    assert module.state(widget) == ['unmuted']

def test_muted_update(module_mock, amixer_mock, mocker):
    mocker.patch(
        'util.cli.execute',
        return_value=amixer_mock(volume='50%', state='off')
    )

    module = module_mock()
    widget = module.widget()

    module.update()
    assert widget.full_text() == '50%'
    assert module.state(widget) == ['warning', 'muted']

def test_exception_update(module_mock, mocker):
    mocker.patch(
        'util.cli.execute',
        side_effect=Exception
    )

    module = module_mock()
    widget = module.widget()

    module.update()
    assert widget.full_text() == 'n/a'

def test_unavailable_amixer(module_mock, mocker):
    mocker.patch('util.cli.execute', return_value='Invalid')

    module = module_mock()
    widget = module.widget()

    module.update()
    assert widget.full_text() == '0%'

def test_toggle(module_mock, mocker):
    command = mocker.patch('util.cli.execute')
    module = module_mock()
    module.toggle(False)
    command.assert_called_once_with('amixer -q set Master,0 toggle')

def test_default_volume(module_mock, mocker):
    module = module_mock()

    command = mocker.patch('util.cli.execute')
    module.increase_volume(False)
    command.assert_called_once_with('amixer -q set Master,0 4%+')

    command = mocker.patch('util.cli.execute')
    module.decrease_volume(False)
    command.assert_called_once_with('amixer -q set Master,0 4%-')

def test_custom_volume(module_mock, mocker):
    module = module_mock(['-p', 'amixer.percent_change=25'])

    command = mocker.patch('util.cli.execute')
    module.increase_volume(False)
    command.assert_called_once_with('amixer -q set Master,0 25%+')

    command = mocker.patch('util.cli.execute')
    module.decrease_volume(False)
    command.assert_called_once_with('amixer -q set Master,0 25%-')

def test_custom_device(module_mock, mocker):
    mocker.patch('util.cli.execute')
    module = module_mock(['-p', 'amixer.device=CustomMaster'])

    command = mocker.patch('util.cli.execute')
    module.toggle(False)
    command.assert_called_once_with('amixer -q set CustomMaster toggle')

    command = mocker.patch('util.cli.execute')
    module.increase_volume(False)
    command.assert_called_once_with('amixer -q set CustomMaster 4%+')

    command = mocker.patch('util.cli.execute')
    module.decrease_volume(False)
    command.assert_called_once_with('amixer -q set CustomMaster 4%-')


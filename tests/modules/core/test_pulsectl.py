from types import SimpleNamespace

import pytest
import pulsectl

import core.config
import core.event
from modules.core import pulsein, pulseout


@pytest.fixture(params=[pulseout, pulsein], ids=["pulseout", "pulsein"])
def audio_module(request, mocker):
    core.event.clear()
    pulse = mocker.MagicMock()
    pulse.__enter__.return_value = pulse
    device = SimpleNamespace(
        name="test-device", volume=SimpleNamespace(value_flat=0.25), mute=False
    )
    pulse.sink_list.return_value = [device]
    pulse.source_list.return_value = [device]
    pulse.server_info.return_value = SimpleNamespace(
        default_sink_name=device.name, default_source_name=device.name
    )
    factory = mocker.patch("modules.core.pulsectl.pulsectl.Pulse", return_value=pulse)
    config = core.config.Config(["-c", "/dev/null"])
    yield request.param.Module, config, factory, pulse, device
    core.event.clear()


def test_recovers_after_server_restart(audio_module):
    cls, config, factory, pulse, device = audio_module
    module = cls(config, None)
    original_widget = module.widget()
    assert original_widget.full_text() == "25%"

    pulse.event_listen.side_effect = pulsectl.PulseDisconnected()
    module.internal_update()
    assert module.widget() is original_widget
    assert module.widget().full_text() == "disconnected"
    assert module.state(None) == ["warning"]

    # The next scheduled update can arrive before the server is ready.
    factory.side_effect = pulsectl.PulseError("Failed to connect")
    module.internal_update()
    assert module.widget() is original_widget
    assert module.widget().full_text() == "disconnected"

    factory.side_effect = None
    pulse.event_listen.side_effect = None
    device.volume.value_flat = 0.6
    device.mute = True
    module.internal_update()

    # Reconnecting must refresh the values without waiting for another event.
    assert module.widget().full_text() == "60%"
    assert module.state(None) == ["warning", "muted"]
    assert pulse.event_listen.call_count == 2

    # The replacement subscription still handles subsequent volume changes.
    device.volume.value_flat = 0.4
    device.mute = False
    callback = pulse.event_callback_set.call_args[0][0]
    callback(None)
    assert module.widget().full_text() == "40%"
    assert module.state(None) == ["unmuted"]


def test_starts_while_server_is_unavailable(audio_module):
    cls, config, factory, pulse, device = audio_module
    factory.side_effect = pulsectl.PulseError("Failed to connect")
    module = cls(config, None)
    assert module.widget().full_text() == "disconnected"
    assert module.state(None) == ["warning"]

    factory.side_effect = None
    module.internal_update()
    assert module.widget().full_text() == "25%"
    assert module.state(None) == ["unmuted"]


def test_device_query_failure_can_recover(audio_module):
    cls, config, factory, pulse, device = audio_module
    module = cls(config, None)
    pulse.server_info.side_effect = pulsectl.PulseOperationFailed("disconnected")
    module.process(None)
    assert module.widget().full_text() == "disconnected"

    pulse.server_info.side_effect = None
    module.process(None)
    assert module.widget().full_text() == "25%"


def test_unexpected_errors_still_reach_core_error_handler(audio_module):
    cls, config, factory, pulse, device = audio_module
    module = cls(config, None)
    pulse.event_listen.side_effect = ValueError("unexpected bug")
    module.internal_update()
    assert module.widget().full_text() == "error: unexpected bug"

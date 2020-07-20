import pytest

import core.config
import modules.contrib.mpd


@pytest.fixture
def mpd_module():
    return modules.contrib.mpd.Module(config=core.config.Config([]), theme=None)


def _test_state(mocker, mpd_module, widget_name, expected_output):
    widget = mocker.Mock()
    widget.name = widget_name
    return mpd_module.state(widget) == expected_output


def test_states(mocker, mpd_module):
    assert _test_state(mocker, mpd_module, "mpd.repeat", "repeat-off")
    assert _test_state(mocker, mpd_module, "mpd.shuffle", "shuffle-off")
    assert _test_state(mocker, mpd_module, "mpd.prev", "prev")
    assert _test_state(mocker, mpd_module, "mpd.next", "next")


def test_no_host(mpd_module):
    assert mpd_module._hostcmd == ""


def test_host():
    module_with_host = modules.contrib.mpd.Module(
        config=core.config.Config(["-p", "mpd.host=sample-host"]), theme=None
    )
    assert module_with_host._hostcmd == " -h sample-host"


def test_host2(mocker):
    cli = mocker.patch("modules.contrib.mpd.util.cli")
    module_with_host = modules.contrib.mpd.Module(
        config=core.config.Config(["-p", "mpd.host=sample-host"]), theme=None
    )
    module_with_host.update()
    args, kwargs = cli.execute.call_args

    assert " -h sample-host" in args[0] and "mpc" in args[0]


def test_bad_layout():
    pytest.raises(
        KeyError,
        modules.contrib.mpd.Module,
        config=core.config.Config(["-p", 'mpd.layout="mpd.inexistent"']),
        theme=None,
    )


def test_hidden_on_creation(mpd_module):
    assert mpd_module.hidden()


def test_update_calls_load_song(mocker, mpd_module):
    mocker.patch.object(mpd_module, "_load_song")
    mpd_module.update()
    mpd_module._load_song.assert_called_with()


def test_default_layout(mpd_module):
    assert mpd_module._layout == "mpd.prev mpd.main mpd.next mpd.shuffle mpd.repeat"


def test_load_module():
    __import__("modules.contrib.mpd")


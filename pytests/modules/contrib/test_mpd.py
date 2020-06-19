import pytest

import core.config
import modules.contrib.mpd

@pytest.fixture
def mpd_module():
    return modules.contrib.mpd.Module(config=core.config.Config([]), theme=None)

def test_shuffle_off_by_default(mpd_module):
    assert not mpd_module._shuffle

def test_shuffle_state(mocker, mpd_module):
    widget = mocker.Mock()
    widget.name = 'mpd.shuffle'
    assert mpd_module.state(widget) == 'shuffle-off'

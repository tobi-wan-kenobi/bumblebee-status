import pytest

import util.cli
import core.config
import modules.contrib.solaar


@pytest.fixture
def module():
    module = modules.contrib.solaar.Module(
        config=core.config.Config([]),
        theme=None
    )

    yield module


def test_load_module():
    __import__("modules.contrib.solaar")


def test_with_unknown_code(module, mocker):
    mocker.patch('util.cli.execute', return_value=(99, 'error'))
    logger = mocker.patch('logging.error')

    module.update()

    logger.assert_called_with('solaar exited with {}: {}'.format(99, 'error'))

    widget = module.widget()
    assert module.state(widget) == 'warning'
    assert module.hidden() == False

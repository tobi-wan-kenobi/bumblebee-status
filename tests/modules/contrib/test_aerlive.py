import pytest

from core.config import Config
from core.input import LEFT_MOUSE, RIGHT_MOUSE
from modules.contrib.aerlive import Module, Measurement


@pytest.fixture
def mock_data():
    return {
        "measurements": [
            Measurement("city1", 15, 30),
            Measurement("city2", 78, 90),
            Measurement("city3", 32, 50),
        ],
        "expected_index": 1, 
    }


def build_module():
    return Module(
        config=Config([]),
        theme=None,
    )


def test_load_module():
    __import__("modules.contrib.aerlive")


def test_input_registration(mocker):
    input_register = mocker.patch("core.input.register")
    module = build_module()

    input_register.assert_any_call(
        module,
        button=LEFT_MOUSE,
        cmd=module.next_location,
    )

    input_register.assert_any_call(
        module,
        button=RIGHT_MOUSE,
        cmd=module.reset_location,
    )

def test_initial_full_text(mocker):
    module = build_module()
    assert module.widget().full_text() == "?"


def test_update_full_text(mock_data, mocker):
    mock_event = mocker.MagicMock()
    module = build_module()

    module.text(mock_event)
    assert module.widget().full_text() == "?"

    module.measurements = mock_data["measurements"]
    module.current_index = mock_data["expected_index"]

    module.text(mock_event)
    assert module.widget().full_text() == "city2 78"


def test_reset_measurement_index(mock_data, mocker):
    module = build_module()

    module.reset_measurement_index()
    assert not module.measurements and module.current_index == -1

    module.measurements = mock_data["measurements"]
    module.reset_measurement_index()
    assert module.measurements and module.current_index == mock_data["expected_index"]

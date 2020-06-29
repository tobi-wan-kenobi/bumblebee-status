import pytest

import core.input


@pytest.fixture
def obj():
    return core.input.Object()


@pytest.fixture
def obj2():
    return core.input.Object()


@pytest.fixture
def cb(mocker):
    return mocker.MagicMock()


@pytest.fixture
def cb2(mocker):
    return mocker.MagicMock()


def event(input_object):
    return {"button": core.input.LEFT_MOUSE, "instance": input_object.id}


def event2(input_object):
    return {"button": core.input.RIGHT_MOUSE, "instance": input_object.id}


def test_callable_gets_called(obj, cb):
    core.input.register(obj, event(obj)["button"], cb)
    core.input.trigger(event(obj))

    cb.assert_called_once_with(event(obj))


def test_nonexistent_callback(obj, obj2, cb):
    core.input.register(obj, event(obj)["button"], cb)
    core.input.trigger(event(obj2))

    cb.assert_not_called()


def test_different_events(obj, obj2, cb, cb2):
    core.input.register(obj, event(obj)["button"], cb)
    core.input.register(obj, event2(obj)["button"], cb)
    core.input.register(obj2, event(obj)["button"], cb2)
    core.input.register(obj2, event2(obj)["button"], cb2)

    core.input.trigger(event(obj))
    core.input.trigger(event2(obj))

    cb.assert_any_call(event(obj))
    cb.assert_any_call(event2(obj))
    cb2.assert_not_called()


def test_multiple_registrations_on_same_button(obj, cb, cb2):
    core.input.register(obj, event(obj)["button"], cb)
    core.input.register(obj, event(obj)["button"], cb2)

    core.input.trigger(event(obj))

    cb2.assert_called_once_with(event(obj))
    cb.assert_not_called()


def test_event_names():
    assert core.input.button_name(core.input.LEFT_MOUSE) == "left-mouse"
    assert core.input.button_name(core.input.RIGHT_MOUSE) == "right-mouse"
    assert core.input.button_name(core.input.MIDDLE_MOUSE) == "middle-mouse"
    assert core.input.button_name(core.input.WHEEL_UP) == "wheel-up"
    assert core.input.button_name(core.input.WHEEL_DOWN) == "wheel-down"
    assert core.input.button_name(12345) == "n/a"


def test_non_callable_callback(mocker, obj):
    cli = mocker.patch("core.input.util.cli")
    cli.execute.return_value = ""

    core.input.register(obj, event(obj)["button"], "sample-command")

    core.input.trigger(event(obj))

    cli.execute.assert_called_once_with("sample-command", wait=False, shell=True)


def test_non_existent_callback(mocker, obj):
    cli = mocker.patch("core.input.util.cli")
    cli.execute.return_value = ""
    cli.execute.side_effect = RuntimeError("some-error")

    core.input.register(obj, event(obj)["button"], "sample-command")

    core.input.trigger(event(obj))

    cli.execute.assert_called_once_with("sample-command", wait=False, shell=True)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

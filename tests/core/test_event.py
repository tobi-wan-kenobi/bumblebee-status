import pytest

import core.event


@pytest.fixture
def someEvent():
    class Event:
        def __init__(self):
            core.event.clear()
            self.id = "some event"
            self.called = 0
            self.call_args = []
            self.call_kwargs = []

        def callback(self, *args, **kwargs):
            self.called += 1
            if args:
                self.call_args.append(list(args))
            if kwargs:
                self.call_kwargs.append(kwargs)

    return Event()


def test_simple_callback(someEvent):
    assert someEvent.called == 0

    core.event.register(someEvent.id, someEvent.callback)
    core.event.register(someEvent.id, someEvent.callback)

    core.event.trigger(someEvent.id)

    assert someEvent.called == 2


def test_args_callback(someEvent):
    core.event.register(someEvent.id, someEvent.callback, "a", "b")
    core.event.trigger(someEvent.id)

    assert someEvent.called == 1
    assert len(someEvent.call_args) == 1
    assert someEvent.call_args[0] == ["a", "b"]


def test_kwargs_callback(someEvent):
    core.event.register(
        someEvent.id, someEvent.callback, "a", "b", key1="test", key2="another"
    )
    core.event.trigger(someEvent.id)

    assert someEvent.called == 1
    assert len(someEvent.call_args) == 1
    assert someEvent.call_args[0] == ["a", "b"]
    assert len(someEvent.call_kwargs) == 1
    assert someEvent.call_kwargs[0] == {"key1": "test", "key2": "another"}


def test_arg_trigger(someEvent):
    core.event.register(someEvent.id, someEvent.callback)
    core.event.trigger(someEvent.id, "a", "b")

    assert someEvent.called == 1
    assert len(someEvent.call_args) == 1
    assert someEvent.call_args[0] == ["a", "b"]


def test_kwargs_trigger(someEvent):
    core.event.register(someEvent.id, someEvent.callback)
    core.event.trigger(someEvent.id, "a", "c", key1="test", key2="something")

    assert someEvent.called == 1
    assert len(someEvent.call_args) == 1
    assert someEvent.call_args[0] == ["a", "c"]
    assert len(someEvent.call_kwargs) == 1
    assert someEvent.call_kwargs[0] == {"key1": "test", "key2": "something"}


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

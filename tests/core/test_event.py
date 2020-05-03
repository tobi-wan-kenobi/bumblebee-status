import unittest

import core.event


class event(unittest.TestCase):
    def setUp(self):
        self.someEvent = "event"
        self.called = {}
        self.params = []
        core.event.clear()

    def callback1(self):
        self.called["callback1"] = True

    def callback2(self):
        self.called["callback2"] = True

    def callback_args(self, val1, val2):
        self.called["callback_args"] = True
        self.params = [val1, val2]

    def callback_kwargs(self, val1, val2, key1=None, key2=None):
        self.called["callback_kwargs"] = True
        self.params = [val1, val2, key1, key2]

    def test_simple_callback(self):
        core.event.register(self.someEvent, self.callback1)
        core.event.register(self.someEvent, self.callback2)

        core.event.trigger(self.someEvent)

        self.assertEqual(2, len(self.called.keys()))

    def test_arg_callback(self):
        core.event.register(self.someEvent, self.callback_args, "a", "b")
        core.event.trigger(self.someEvent)
        self.assertEqual(1, len(self.called.keys()))
        self.assertEqual(["a", "b"], self.params)

    def test_kwargs_callback(self):
        core.event.register(
            self.someEvent, self.callback_kwargs, "a", "b", key1="test", key2="x"
        )
        core.event.trigger(self.someEvent)
        self.assertEqual(1, len(self.called.keys()))
        self.assertEqual(["a", "b", "test", "x"], self.params)

    def test_arg_trigger(self):
        core.event.register(self.someEvent, self.callback_args)
        core.event.trigger(self.someEvent, "a", "b")
        self.assertEqual(1, len(self.called.keys()))
        self.assertEqual(["a", "b"], self.params)

    def test_kwargs_trigger(self):
        core.event.register(self.someEvent, self.callback_kwargs)
        core.event.trigger(self.someEvent, "a", "b", key1="test", key2="x")
        self.assertEqual(1, len(self.called.keys()))
        self.assertEqual(["a", "b", "test", "x"], self.params)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

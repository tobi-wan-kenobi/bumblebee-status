import unittest

import core.input

class config(unittest.TestCase):
    def setUp(self):
        self.inputObject = core.input.Object()
        self.anotherObject = core.input.Object()
        self.someEvent = { 'button': core.input.LEFT_MOUSE, 'instance': self.inputObject.id() }
        self.anotherEvent = { 'button': core.input.RIGHT_MOUSE, 'instance': self.inputObject.id() }
        self.callback = unittest.mock.MagicMock()
        self.callback2 = unittest.mock.MagicMock()

    def test_callable_gets_called(self):
        core.input.register(self.inputObject, self.someEvent['button'], self.callback)
        core.input.trigger(self.someEvent)
        self.callback.assert_called_once_with(self.someEvent)

    def test_different_events(self):
        core.input.register(self.inputObject, self.someEvent['button'], self.callback)
        core.input.register(self.inputObject, self.anotherEvent['button'], self.callback)
        core.input.register(self.anotherObject, self.someEvent['button'], self.callback2)
        core.input.register(self.anotherObject, self.anotherEvent['button'], self.callback2)
        core.input.trigger(self.someEvent)
        core.input.trigger(self.anotherEvent)
        self.callback.assert_any_call(self.someEvent)
        self.callback.assert_any_call(self.anotherEvent)
        self.callback2.assert_not_called()

    def test_multiple_registrations(self):
        core.input.register(self.inputObject, self.someEvent['button'], self.callback)
        core.input.register(self.inputObject, self.someEvent['button'], self.callback2)
        core.input.trigger(self.someEvent)
        self.callback.assert_called_once_with(self.someEvent)
        self.callback2.assert_called_once_with(self.someEvent)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

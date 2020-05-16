import unittest

import core.input


class config(unittest.TestCase):
    def setUp(self):
        self.inputObject = core.input.Object()
        self.anotherObject = core.input.Object()
        self.someEvent = {
            "button": core.input.LEFT_MOUSE,
            "instance": self.inputObject.id,
        }
        self.anotherEvent = {
            "button": core.input.RIGHT_MOUSE,
            "instance": self.inputObject.id,
        }
        self.callback = unittest.mock.MagicMock()
        self.callback2 = unittest.mock.MagicMock()
        self.someCommand = "some sample command"

    def test_callable_gets_called(self):
        core.input.register(self.inputObject, self.someEvent["button"], self.callback)
        core.input.trigger(self.someEvent)
        self.callback.assert_called_once_with(self.someEvent)

    def test_nonexistent_callback(self):
        core.input.register(self.inputObject, self.someEvent["button"], self.callback)
        core.input.trigger(self.anotherEvent)
        self.callback.assert_not_called()

    def test_different_events(self):
        core.input.register(self.inputObject, self.someEvent["button"], self.callback)
        core.input.register(
            self.inputObject, self.anotherEvent["button"], self.callback
        )
        core.input.register(
            self.anotherObject, self.someEvent["button"], self.callback2
        )
        core.input.register(
            self.anotherObject, self.anotherEvent["button"], self.callback2
        )
        core.input.trigger(self.someEvent)
        core.input.trigger(self.anotherEvent)
        self.callback.assert_any_call(self.someEvent)
        self.callback.assert_any_call(self.anotherEvent)
        self.callback2.assert_not_called()

    def test_multiple_registrations(self):
        core.input.register(self.inputObject, self.someEvent["button"], self.callback)
        core.input.register(self.inputObject, self.someEvent["button"], self.callback2)
        core.input.trigger(self.someEvent)
        self.callback.assert_called_once_with(self.someEvent)
        self.callback2.assert_called_once_with(self.someEvent)

    def test_event_names(self):
        self.assertEqual(core.input.button_name(core.input.LEFT_MOUSE), "left-mouse")
        self.assertEqual(core.input.button_name(core.input.RIGHT_MOUSE), "right-mouse")
        self.assertEqual(
            core.input.button_name(core.input.MIDDLE_MOUSE), "middle-mouse"
        )
        self.assertEqual(core.input.button_name(core.input.WHEEL_UP), "wheel-up")
        self.assertEqual(core.input.button_name(core.input.WHEEL_DOWN), "wheel-down")
        self.assertEqual(core.input.button_name(12345), "n/a")

    def test_non_callable_callback(self):
        with unittest.mock.patch("core.input.util.cli") as cli:
            cli.execute.return_value = ""
            core.input.register(
                self.inputObject, self.someEvent["button"], self.someCommand
            )
            core.input.trigger(self.someEvent)
            cli.execute.assert_called_once_with(
                self.someCommand, wait=False, shell=True
            )

    def test_non_existent_callback(self):
        with unittest.mock.patch("core.input.util.cli") as cli:
            cli.execute.return_value = ""
            cli.execute.side_effect = RuntimeError("some-error")
            core.input.register(
                self.inputObject, self.someEvent["button"], self.someCommand
            )
            try:
                core.input.trigger(self.someEvent)
            except Exception:
                self.fail("input module propagated exception")


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

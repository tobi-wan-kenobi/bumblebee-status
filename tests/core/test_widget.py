import unittest
import unittest.mock

import core.widget
import core.module
import core.config


class TestModule(core.module.Module):
    def __init__(self, widgets, config=core.config.Config([]), theme=None):
        super().__init__(config, theme, widgets)
        self.states = []

    def update(self):
        if self.fail:
            raise Exception(self.error)
        pass

    def state(self, widget):
        return self.states


class widget(unittest.TestCase):
    def setUp(self):
        self.someValue = "some random value"
        self.someOtherValue = "some different value"
        self.callbackReturnValue = "callback return value"
        self.someWidget = core.widget.Widget(full_text=self.someValue)
        self.someCallback = unittest.mock.MagicMock(
            return_value=self.callbackReturnValue
        )

        self.assertNotEqual(self.someValue, self.someOtherValue)

    def tearDown(self):
        pass

    def test_text_fulltext(self):
        newWidget = core.widget.Widget(full_text=self.someValue)
        self.assertEqual(self.someValue, newWidget.full_text())

    def test_set_fulltext(self):
        self.assertNotEqual(self.someOtherValue, self.someWidget.full_text())
        self.someWidget.full_text(self.someOtherValue)
        self.assertEqual(self.someOtherValue, self.someWidget.full_text())

    def test_callable_fulltext(self):
        newWidget = core.widget.Widget(full_text=self.someCallback)
        self.assertEqual(newWidget.full_text(), self.callbackReturnValue)
        self.someCallback.assert_called_once_with(newWidget)

    def test_set_callable_fulltext(self):
        self.someWidget.full_text(self.someCallback)
        self.assertEqual(self.someWidget.full_text(), self.callbackReturnValue)
        self.someCallback.assert_called_once_with(self.someWidget)

    def test_state_defaults_to_empty(self):
        self.assertEqual([], self.someWidget.state())

    def test_single_widget_state(self):
        self.someWidget.set("state", "state1")
        self.assertEqual(["state1"], self.someWidget.state())

    def test_multiple_widget_states(self):
        self.someWidget.set("state", ["state1", "state2"])
        self.assertEqual(["state1", "state2"], self.someWidget.state())

    def test_widget_module_state(self):
        module = TestModule(widgets=self.someWidget)
        self.someWidget.set("state", ["state1", "state2"])

        module.states = "x"
        self.assertEqual(["state1", "state2", "x"], self.someWidget.state())
        module.states = ["a", "b"]
        self.assertEqual(["state1", "state2", "a", "b"], self.someWidget.state())

    def test_multiple_widget_themes(self):
        widget1 = core.widget.Widget(full_text="a")
        widget2 = core.widget.Widget(full_text="b")
        widget3 = core.widget.Widget(full_text="c")

        module = TestModule(widgets=[widget1, widget2, widget3])
        module.set("theme.test", "1,2,3")
        module.set("theme.test2", "x")

        self.assertEqual("1", widget1.theme("test"))
        self.assertEqual("2", widget2.theme("test"))
        self.assertEqual("3", widget3.theme("test"))

        self.assertEqual("x", widget1.theme("test2"))
        self.assertEqual(None, widget2.theme("test2"))
        self.assertEqual(None, widget3.theme("test2"))


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

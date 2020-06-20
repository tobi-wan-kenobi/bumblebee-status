import pytest

import core.widget
import core.module
import core.config


class SampleModule(core.module.Module):
    def __init__(self, widgets, config=core.config.Config([]), theme=None):
        super().__init__(config, theme, widgets)
        self.states = []

    def update(self):
        if self.fail:
            raise Exception(self.error)
        pass

    def state(self, widget):
        return self.states


@pytest.fixture
def widget_a():
    return core.widget.Widget("some random value")


# class widget(unittest.TestCase):
#    def setUp(self):
#        self.someValue = "some random value"
#        self.someOtherValue = "some different value"
#        self.callbackReturnValue = "callback return value"
#        self.someWidget = core.widget.Widget(full_text=self.someValue)
#        self.someCallback = unittest.mock.MagicMock(
#            return_value=self.callbackReturnValue
#        )
#
#        self.assertNotEqual(self.someValue, self.someOtherValue)


def test_text_fulltext():
    widget = core.widget.Widget(full_text="this is some value")
    assert widget.full_text() == "this is some value"


def test_set_fulltext(widget_a):
    assert widget_a.full_text() != "new value"
    widget_a.full_text("new value")
    assert widget_a.full_text() == "new value"


def test_callable_fulltext(mocker):
    callback = mocker.MagicMock(return_value="callback returns")
    widget = core.widget.Widget(full_text=callback)
    assert widget.full_text() == "callback returns"
    callback.assert_called_once_with(widget)


def test_set_callable_fulltext(mocker, widget_a):
    callback = mocker.MagicMock(return_value="this is a test")
    widget_a.full_text(callback)
    assert widget_a.full_text() == "this is a test"
    callback.assert_called_once_with(widget_a)


def test_state_defaults_to_empty(widget_a):
    assert widget_a.state() == []


def test_single_widget_state(widget_a):
    widget_a.set("state", "state1")
    assert widget_a.state() == ["state1"]


def test_multiple_widget_states(widget_a):
    widget_a.set("state", ["state1", "state2"])
    assert widget_a.state() == ["state1", "state2"]


def test_widget_module_state(widget_a):
    module = SampleModule(widgets=widget_a)
    widget_a.set("state", ["state1", "state2"])

    module.states = "x"
    assert widget_a.state() == ["state1", "state2", "x"]

    module.states = ["a", "b"]
    assert widget_a.state() == ["state1", "state2", "a", "b"]


def test_multiple_widget_themes():
    widget1 = core.widget.Widget(full_text="a")
    widget2 = core.widget.Widget(full_text="b")
    widget3 = core.widget.Widget(full_text="c")

    module = SampleModule(widgets=[widget1, widget2, widget3])
    module.set("theme.test", "1,2,3")
    module.set("theme.test2", "x")

    assert widget1.theme("test") == "1"
    assert widget2.theme("test") == "2"
    assert widget3.theme("test") == "3"

    assert widget1.theme("test2") == "x"
    assert widget2.theme("test2") == None
    assert widget3.theme("test2") == None


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

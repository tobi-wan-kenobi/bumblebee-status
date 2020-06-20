import pytest

import core.decorators
import core.widget
import core.module
import core.config


@pytest.fixture
def module():
    class TestModule(core.module.Module):
        @core.decorators.never
        def __init__(self, config=None, theme=None):
            config = core.config.Config([])
            super().__init__(config, theme, core.widget.Widget(self.get))
            self.text = ""

        @core.decorators.scrollable
        def get(self, widget):
            return self.text

    module = TestModule()
    module.set("scrolling.width", 10)
    return module


def test_never(module):
    assert module.parameter("interval") == "never"


def test_no_text(module):
    assert module.text == ""
    assert module.get(module.widget()) == ""


def test_smaller(module):
    module.text = "test"
    assert module.parameter("scrolling.width") > len(module.text)
    assert module.get(module.widget()) == module.text


def test_bigger(module):
    module.text = "this is a really really long sample text"
    maxwidth = module.parameter("scrolling.width")
    assert maxwidth < len(module.text)
    assert module.get(module.widget()) == module.text[:maxwidth]


def test_bounce(module):
    module.text = "abcd"
    module.set("scrolling.width", 2)
    assert module.get(module.widget()) == "ab"
    assert module.get(module.widget()) == "bc"
    assert module.get(module.widget()) == "cd"
    assert module.get(module.widget()) == "bc"
    assert module.get(module.widget()) == "ab"
    assert module.get(module.widget()) == "bc"
    assert module.get(module.widget()) == "cd"
    assert module.get(module.widget()) == "bc"
    assert module.get(module.widget()) == "ab"


def test_nobounce(module):
    module.set("scrolling.bounce", False)
    module.set("scrolling.width", 2)
    module.text = "abcd"

    assert module.get(module.widget()) == "ab"
    assert module.get(module.widget()) == "bc"
    assert module.get(module.widget()) == "cd"
    assert module.get(module.widget()) == "ab"
    assert module.get(module.widget()) == "bc"
    assert module.get(module.widget()) == "cd"


def test_completely_changed_data(module):
    module.text = "abcd"
    module.set("scrolling.width", 2)

    assert module.get(module.widget()) == "ab"
    assert module.get(module.widget()) == "bc"

    module.text = "wxyz"
    assert module.get(module.widget()) == "wx"
    assert module.get(module.widget()) == "xy"


def test_slightly_changed_data(module):
    module.text = "this is a sample song (0:00)"
    module.set("scrolling.width", 10)

    assert module.get(module.widget()) == module.text[0:10]
    module.text = "this is a sample song (0:01)"
    assert module.get(module.widget()) == module.text[1:11]
    module.text = "this is a sample song (0:02)"
    assert module.get(module.widget()) == module.text[2:12]
    module.text = "this is a sample song (0:13)"
    assert module.get(module.widget()) == module.text[3:13]
    module.text = "this is a different song (0:13)"
    assert module.get(module.widget()) == module.text[0:10]


def test_n_plus_one(module):
    module.text = "10 letters"
    module.set("scrolling.width", 9)

    assert module.get(module.widget()) == module.text[0:9]
    assert module.get(module.widget()) == module.text[1:10]
    assert module.get(module.widget()) == module.text[0:9]
    assert module.get(module.widget()) == module.text[1:10]
    assert module.get(module.widget()) == module.text[0:9]


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

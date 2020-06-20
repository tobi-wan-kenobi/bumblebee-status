import pytest
import types

import core.theme
import core.event
import core.widget
import core.module


class SampleModule(core.module.Module):
    def __init__(self, widgets, config=core.config.Config([]), theme=None):
        super().__init__(config, theme, widgets)
        self.name = "test"


@pytest.fixture(autouse=True)
def clear_events():
    core.event.clear()


@pytest.fixture
def defaultsTheme():
    return {"defaults": {"fg": "red", "bg": "black"}}


@pytest.fixture
def cycleTheme():
    return {
        "cycle": [
            {"fg": "red", "bg": "black"},
            {"fg": "black", "bg": "red"},
            {"fg": "white", "bg": "blue"},
        ]
    }


@pytest.fixture
def colorTheme():
    return {"colors": [{"red": "#ff0000", "blue": "#0000ff"}]}


@pytest.fixture
def walTheme():
    return {"colors": ["wal"]}


@pytest.fixture
def cycleValueTheme():
    return {"defaults": {"fg": ["red", "green", "blue"]}}


@pytest.fixture
def stateTheme():
    return {"warning": {"fg": "yellow"}, "critical": {"fg": "red"}}


@pytest.fixture
def overlayTheme():
    return {
        "load": {"prefix": "a"},
        "test": {"load": {"prefix": "b"}, "prefix": "x"},
    }


def test_invalid_theme():
    with pytest.raises(RuntimeError):
        core.theme.Theme("this-theme-does-not-exist")


def test_valid_theme():
    theme = core.theme.Theme("default")
    assert theme.name == "default"


def test_defaults(defaultsTheme):
    theme = core.theme.Theme(raw_data=defaultsTheme)

    assert theme.get("fg") == defaultsTheme["defaults"]["fg"]
    assert theme.get("bg") == defaultsTheme["defaults"]["bg"]


def test_cycle(mocker, cycleTheme):
    theme = core.theme.Theme(raw_data=cycleTheme)

    assert theme.get("bg", "previous") == None
    assert theme.get("fg") == cycleTheme["cycle"][0]["fg"]
    assert theme.get("bg") == cycleTheme["cycle"][0]["bg"]

    core.event.trigger("next-widget")

    assert theme.get("bg", "previous") == cycleTheme["cycle"][0]["bg"]

    core.event.trigger("next-widget")

    assert theme.get("fg") == cycleTheme["cycle"][2]["fg"]
    assert theme.get("bg") == cycleTheme["cycle"][2]["bg"]

    stdout = mocker.patch("core.output.sys.stdout")

    core.event.trigger("draw")

    assert theme.get("fg") == cycleTheme["cycle"][0]["fg"]
    assert theme.get("bg") == cycleTheme["cycle"][0]["bg"]


def test_custom_iconset(defaultsTheme):
    theme = core.theme.Theme(raw_data=defaultsTheme)

    assert theme.get("padding") != "aaa"
    assert theme.get("fg") != "blue"

    theme = core.theme.Theme(
        raw_data=defaultsTheme, iconset={"defaults": {"padding": "aaa", "fg": "blue"}}
    )

    assert theme.get("padding") == "aaa"
    assert theme.get("fg") == "blue"  # test override


def test_colors(defaultsTheme, colorTheme):
    theme = core.theme.Theme(raw_data=defaultsTheme)
    assert theme.keywords() == {}

    theme = core.theme.Theme(raw_data=colorTheme)
    assert theme.keywords() == colorTheme["colors"][0]


def test_wal_colors(mocker, walTheme):
    io = mocker.patch("core.theme.io")
    os = mocker.patch("core.theme.os")

    os.path.isfile.return_value = True
    io.open.return_value = mocker.MagicMock()
    io.open.return_value.__enter__.return_value.read.return_value = """
        { "colors": { "red": "#ff0000" } }
    """

    theme = core.theme.Theme(raw_data=walTheme)

    assert theme.keywords() == {"red": "#ff0000"}


def test_wal_special(mocker, walTheme):
    io = mocker.patch("core.theme.io")
    os = mocker.patch("core.theme.os")

    os.path.isfile.return_value = True
    io.open.return_value.__enter__.return_value.read.return_value = """
        { "special": { "background": "#ff0000" } }
    """

    theme = core.theme.Theme(raw_data=walTheme)

    assert theme.keywords() == {"background": "#ff0000"}


def test_cycle_value(cycleValueTheme):
    widget = core.widget.Widget()
    expected = cycleValueTheme["defaults"]["fg"]
    theme = core.theme.Theme(raw_data=cycleValueTheme)

    for i in range(0, len(expected) * 3):
        assert theme.get("fg", widget) == expected[i % len(expected)]
        # ensure multiple invocations are OK
        assert theme.get("fg", widget) == expected[i % len(expected)]
        core.event.trigger("draw")


def test_state(stateTheme):
    widget = core.widget.Widget()
    theme = core.theme.Theme(raw_data=stateTheme)

    assert theme.get("fg", widget) == None

    widget.state = types.MethodType(lambda self: ["warning"], widget)
    assert theme.get("fg", widget) == stateTheme["warning"]["fg"]

    widget.state = types.MethodType(lambda self: ["critical"], widget)
    assert theme.get("fg", widget) == stateTheme["critical"]["fg"]


def test_overlay(overlayTheme):
    widget = core.widget.Widget()
    module = SampleModule(widget)
    theme = core.theme.Theme(raw_data=overlayTheme)

    assert theme.get("prefix", widget) == overlayTheme[module.name]["prefix"]

    widget.state = types.MethodType(lambda self: ["load"], widget)

    assert theme.get("prefix", widget) == overlayTheme[module.name]["load"]["prefix"]


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

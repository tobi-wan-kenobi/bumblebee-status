import pytest
import types
from unittest.mock import MagicMock

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


def _make_mock_widget(widget_id="test-widget", states=None):
    w = MagicMock(spec=[])
    w.id = widget_id
    w.module = None
    w.state = MagicMock(return_value=states if states is not None else [])
    # Ensure _state_cache is not present so widget.state() is called
    return w


def test_cache_hit_skips_cascade(mocker):
    """Second get() for same (widget, state, count) returns cached value, not re-resolved."""
    theme = core.theme.Theme(raw_data={"defaults": {"fg": "#original"}})
    widget = _make_mock_widget("w1", [])

    first = theme.get("fg", widget)
    assert first == "#original"

    # Mutate the theme data — if cache is bypassed, second call would return "#mutated"
    theme._Theme__data["defaults"]["fg"] = "#mutated"

    second = theme.get("fg", widget)
    assert second == "#original"  # still returns cached value


def test_list_values_not_cached():
    """List values (cycling colors) are excluded from the cache."""
    theme = core.theme.Theme(raw_data={"defaults": {"fg": ["#aaa", "#bbb"]}})
    widget = _make_mock_widget("w1", [])
    widget.set = MagicMock()  # list path calls widget.set(key, idx)

    theme.get("fg", widget)

    # List values must not be in __resolved (they cycle per tick)
    cache = theme._Theme__resolved
    for cache_key, entry in cache.items():
        if cache_key[0] == "w1":
            assert "fg" not in entry


def test_cache_different_states_produce_different_entries():
    """Different states on the same widget id produce separate cached entries."""
    theme = core.theme.Theme(
        raw_data={"defaults": {"fg": "#aabbcc"}, "warning": {"fg": "#ff0000"}}
    )
    widget_normal = _make_mock_widget(widget_id="w2", states=[])
    widget_warning = _make_mock_widget(widget_id="w2", states=["warning"])

    result_normal = theme.get("fg", widget_normal)
    result_warning = theme.get("fg", widget_warning)

    assert result_normal == "#aabbcc"
    assert result_warning == "#ff0000"
    # Two distinct cache keys for the same widget id
    keys_for_w2 = [k for k in theme._Theme__resolved if k[0] == "w2"]
    assert len(keys_for_w2) == 2


def test_invalidate_widget_removes_cache_entries():
    """invalidate_widget evicts all cached entries for the given widget."""
    theme = core.theme.Theme(raw_data={"defaults": {"fg": "#aabbcc"}})
    widget = _make_mock_widget(widget_id="w3", states=[])

    theme.get("fg", widget)
    assert any(k[0] == "w3" for k in theme._Theme__resolved)

    theme.invalidate_widget(widget.id)
    assert not any(k[0] == "w3" for k in theme._Theme__resolved)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

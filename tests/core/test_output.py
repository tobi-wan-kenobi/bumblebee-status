import json
import pytest

import core.event
import core.config
import core.output
import core.module


class SampleModule(core.module.Module):
    pass


@pytest.fixture(autouse=True)
def clear_events():
    core.event.clear()


@pytest.fixture
def i3():
    return core.output.i3()


@pytest.fixture
def module_a(mocker):
    widget = mocker.MagicMock()
    widget.full_text.return_value = "test"
    widget.id = "a"
    widget.hidden = False
    return SampleModule(config=core.config.Config([]), widgets=[widget, widget, widget])

@pytest.fixture
def module_b(mocker):
    widget = mocker.MagicMock()
    widget.full_text.return_value = "test"
    widget.id = "b"
    return SampleModule(config=core.config.Config([]), widgets=[widget, widget, widget])


@pytest.fixture
def paddedTheme():
    return core.theme.Theme(raw_data={"defaults": {"padding": " "}})


@pytest.fixture
def separatorTheme():
    return core.theme.Theme(
        raw_data={"defaults": {"separator": "***", "fg": "red", "bg": "blue"}}
    )


@pytest.fixture
def block_a(separatorTheme, module_a):
    return core.output.block(
        theme=separatorTheme, module=module_a, widget=module_a.widget(),
    )

def test_start(i3):
    all_data = i3.start()
    data = all_data["blocks"]

    assert data["version"] == 1
    assert data["click_events"] == True
    assert all_data["suffix"] == "\n["


def test_stop(i3):
    assert i3.stop()["suffix"] == "\n]"


def test_no_modules_by_default(i3):
    assert i3.modules() == []


def test_register_single_module(i3, module_a):
    i3.modules(module_a)

    assert i3.modules() == [module_a]


def test_register_multiple_modules(i3, module_a):
    i3.modules([module_a, module_a, module_a])
    assert i3.modules() == [module_a, module_a, module_a]

def test_toggle_module(i3, module_a, module_b):
    i3.modules([module_a, module_b])

    i3.update()
    i3.toggle_minimize({ "instance": module_a.widget().id })
    i3.update()

    assert i3.content()[module_a.widget().id]["minimized"] == True

#    assert module_a.widget().minimized == True
#    assert module_b.widget().minimized == False
#
#    i3.toggle_minimize({ "instance": module_a.widget().id })
#    i3.toggle_minimize({ "instance": module_b.widget().id })
#
#    assert module_a.widget().minimized == False
#    assert module_b.widget().minimized == True

def test_draw_existing_module(mocker, i3):
    i3.test_draw = mocker.MagicMock(
        return_value={"blocks": {"test": True}, "suffix": "end"}
    )
    i3.draw("test_draw")
    i3.test_draw.assert_called_once_with()


def test_empty_status_line(i3):
    data = i3.statusline()

    assert data["blocks"] == []
    assert data["suffix"] == ","


def test_statusline(i3, module_a):
    i3.modules([module_a, module_a, module_a])
    i3.update()
    data = i3.statusline()
    assert len(data["blocks"]) == len(module_a.widgets()) * 3


def test_padding(i3, paddedTheme, module_a):
    i3.theme(paddedTheme)
    blk = core.output.block(i3.theme(), module_a, module_a.widget())
    blk.set("full_text", "abc")
    result = blk.dict()["full_text"]
    assert result == " abc "


def test_no_separator(i3, module_a):
    result = i3.separator_block(module_a, module_a.widget())
    assert result == []


def test_separator(i3, separatorTheme, module_a):
    i3.theme(separatorTheme)
    result = i3.separator_block(module_a, module_a.widget())

    assert len(result) == 1
    assert result[0].dict()["full_text"] == "***"
    assert result[0].dict().get("_decorator") == True
    assert result[0].dict()["color"] == separatorTheme.get("bg", module_a.widget())


def test_dump_json(mocker):
    obj = mocker.MagicMock()
    obj.dict = mocker.MagicMock()
    core.output.dump_json(obj)
    obj.dict_assert_called_once_with()


def test_assign():
    src = {"a": "x", "b": "y", "c": "z"}
    dst = {}

    core.output.assign(src, dst, "a")
    assert src["a"] == dst["a"]

    core.output.assign(src, dst, "123", "b")
    assert src["b"] == dst["123"]

    core.output.assign(src, dst, "blub", default="def")
    assert dst["blub"] == "def"


def test_pango_detection(block_a):
    assert block_a.is_pango({}) == False
    assert block_a.is_pango({"pango": {}}) == True


def test_pangoize(block_a):
    assert block_a.pangoize("test") == "test"
    assert not "markup" in block_a.dict()

    pango = block_a.pangoize({"pango": {"attr": "blub", "x": "y", "full_text": "test"}})
    assert 'attr="blub"' in pango
    assert 'x="y"' in pango
    assert "<span " in pango
    assert ">test</span>" in pango
    assert block_a.dict()["markup"] == "pango"


def test_padding(block_a):
    block_a.set("padding", "***")
    block_a.set("full_text", "test")

    assert block_a.dict()["full_text"] == "***test***"


def test_pre_suffix(block_a):
    block_a.set("padding", "*")
    block_a.set("prefix", "pre")
    block_a.set("suffix", "suf")
    block_a.set("full_text", "test")

    assert block_a.dict()["full_text"] == "*pre*test*suf*"


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

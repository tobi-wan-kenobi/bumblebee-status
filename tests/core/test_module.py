import pytest

import sys
import shlex

import core.module
import core.widget
import core.config
import core.input


@pytest.fixture(autouse=True)
def clear_events():
    core.event.clear()


@pytest.fixture
def empty_config():
    return core.config.Config([])


@pytest.fixture
def widget_a():
    return core.widget.Widget("randomwWidget content", name="A")


@pytest.fixture
def widget_b():
    return core.widget.Widget("another randomwWidget content", name="B")


class SampleModule(core.module.Module):
    def update(self):
        if self.fail:
            raise Exception(self.error)
        pass


def test_loadinvalid_module(mocker):
    config = mocker.MagicMock()
    module = core.module.load(module_name="i-do-not-exist", config=config)
    assert module.__class__.__module__ == "core.module"
    assert module.__class__.__name__ == "Error"


@pytest.mark.skipif(
    sys.version_info.major == 3 and sys.version_info.minor in [4, 5],
    reason="importlib error reporting in Python 3.{4,5} different",
)
def test_importerror(mocker):
    importlib = mocker.patch("core.module.importlib")
    importlib.import_module.side_effect = ImportError("some-error")
    config = mocker.MagicMock()

    module = core.module.load(module_name="test", config=config)

    assert module.__class__.__name__ == "Error"
    assert module.widget().full_text() == "test: some-error" or \
        module.widget().full_text() == "test: unable to load module"


def test_loadvalid_module():
    module = core.module.load(module_name="test")
    assert module.__class__.__module__ == "modules.core.test"
    assert module.__class__.__name__ == "Module"
    assert module.state(None) == []


def test_empty_widgets():
    module = core.module.Module(widgets=[])
    assert module.widgets() == []


def test_error_widget():
    cfg = core.config.Config(shlex.split("-p test_module.foo=5"))
    module = core.module.Error("test-mod", "xyz", config=cfg)
    full_text = module.full_text(module.widget())

    assert module.state(None) == ["critical"]
    assert "test-mod" in full_text
    assert "xyz" in full_text


def test_single_widget(widget_a):
    module = core.module.Module(widgets=widget_a)
    assert module.widgets() == [widget_a]


def test_widget_list(widget_a, widget_b):
    module = core.module.Module(widgets=[widget_a, widget_b])
    assert module.widgets() == [widget_a, widget_b]


def test_module_Name():
    module = SampleModule()
    assert module.name == "test_module"
    assert module.module_name == "test_module"


def testvalid_parameter():
    cfg = core.config.Config(shlex.split("-p test_module.foo=5"))
    module = SampleModule(config=cfg)
    assert module.parameter("foo") == "5"


def test_default_parameter(empty_config):
    module = SampleModule(config=empty_config)
    assert module.parameter("foo", "default") == "default"


def test_default_is_none(empty_config):
    module = SampleModule(config=empty_config)
    assert module.parameter("foo") == None


def test_error_widget(empty_config):
    module = SampleModule(config=empty_config)
    module.fail = True
    module.error = "!!"
    module.update_wrapper()
    assert len(module.widgets()) == 1
    assert module.widget().full_text() == "error: !!"


def test_get_widget_by_name(empty_config, widget_a, widget_b):
    module = SampleModule(config=empty_config, widgets=[widget_a, widget_b])

    assert module.widget(widget_a.name) == widget_a
    assert module.widget(widget_b.name) == widget_b
    assert module.widget("i-do-not-exist") == None
    assert module.widget() == widget_a

def test_get_widget_by_id(empty_config, widget_a, widget_b):
    module = SampleModule(config=empty_config, widgets=[widget_a, widget_b])

    assert module.widget(widget_id=widget_a.id) == widget_a
    assert module.widget(widget_id=widget_b.id) == widget_b
    assert module.widget(widget_id="i-do-not-exist") == None


def test_default_thresholds(empty_config, widget_a, widget_b):
    module = SampleModule(config=empty_config, widgets=[widget_a, widget_b])

    assert module.threshold_state(100, 80, 99) == "critical"
    assert module.threshold_state(100, 80, 100) == "warning"
    assert module.threshold_state(81, 80, 100) == "warning"
    assert module.threshold_state(80, 80, 100) == None
    assert module.threshold_state(10, 80, 100) == None


def test_configured_callbacks(mocker, empty_config, widget_a, widget_b):
    module = SampleModule(config=empty_config, widgets=[widget_a, widget_b])

    cmd = "sample-tool arg1 arg2 arg3"
    module.set("left-click", cmd)
    module.register_callbacks()

    cli = mocker.patch("core.input.util.cli")
    cli.execute.return_value = ""
    core.input.trigger(
        {"button": core.input.LEFT_MOUSE, "instance": module.id,}
    )

    cli.execute.assert_called_once_with(cmd, wait=False, shell=True)


def test_configured_callbacks_with_parameters(mocker, empty_config, widget_a):
    module = SampleModule(config=empty_config, widgets=[widget_a])

    cmd = "sample-tool {instance} {name}"
    module.set("left-click", cmd)
    module.register_callbacks()

    cli = mocker.patch("core.input.util.cli")
    cli.execute.return_value = ""
    core.input.trigger(
        {"button": core.input.LEFT_MOUSE, "instance": module.id, "name": "sample-name",}
    )

    cli.execute.assert_called_once_with(
        cmd.format(instance=module.id, name="sample-name"), wait=False, shell=True,
    )


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

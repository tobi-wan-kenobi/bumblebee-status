import unittest

import sys
import shlex

import core.module
import core.widget
import core.config
import core.input


class TestModule(core.module.Module):
    def update(self):
        if self.fail:
            raise Exception(self.error)
        pass


class module(unittest.TestCase):
    def setUp(self):
        self.invalidModuleName = "invalid-module-name"
        self.validModuleName = "test"
        self.someWidget = core.widget.Widget("randomeWidgetContent", name="A")
        self.anotherWidget = core.widget.Widget("more Widget content", name="B")
        self.unusedWidgetName = "C"

    def test_loadinvalid_module(self):
        config = unittest.mock.MagicMock()
        module = core.module.load(module_name=self.invalidModuleName, config=config)
        self.assertEqual(
            "core.module", module.__class__.__module__, "module must be a module object"
        )
        self.assertEqual(
            "Error",
            module.__class__.__name__,
            "an invalid module must be a core.module.Error",
        )

    @unittest.skipIf(
        sys.version_info.major == 3 and sys.version_info.minor in [4, 5],
        "importlib error reporting in Python 3.{4,5} different",
    )
    def test_importerror(self):
        with unittest.mock.patch("core.module.importlib") as importlib:
            importlib.import_module.side_effect = ImportError("some-error")

            config = unittest.mock.MagicMock()
            module = core.module.load(module_name=self.validModuleName, config=config)
            module.widget().full_text()
            self.assertEqual(
                "Error",
                module.__class__.__name__,
                "an invalid module must be a core.module.Error",
            )
            self.assertEqual(module.widget().full_text(), "test: some-error")

    def test_loadvalid_module(self):
        module = core.module.load(module_name=self.validModuleName)
        self.assertEqual(
            "modules.core.{}".format(self.validModuleName),
            module.__class__.__module__,
            "module must be a modules.core.<name> object",
        )
        self.assertEqual(
            "Module",
            module.__class__.__name__,
            "a valid module must have a Module class",
        )
        self.assertEqual([], module.state(None), "default state of module is empty")

    def test_empty_widgets(self):
        module = core.module.Module(widgets=[])
        self.assertEqual([], module.widgets())

    def test_error_widget(self):
        cfg = core.config.Config(shlex.split("-p test_module.foo=5"))
        module = core.module.Error(cfg, "test-mod", "xyz")
        self.assertEqual(
            ["critical"], module.state(None), "error module must have critical state"
        )
        full_text = module.full_text(module.widget())
        self.assertTrue("test-mod" in full_text)
        self.assertTrue("xyz" in full_text)

    def test_single_widget(self):
        module = core.module.Module(widgets=self.someWidget)
        self.assertEqual([self.someWidget], module.widgets())

    def test_widget_list(self):
        module = core.module.Module(widgets=[self.someWidget, self.anotherWidget])
        self.assertEqual([self.someWidget, self.anotherWidget], module.widgets())

    def test_module_Name(self):
        module = TestModule()
        self.assertEqual("test_module", module.name, "module has wrong name")
        self.assertEqual("test_module", module.module_name, "module has wrong name")

    def testvalid_parameter(self):
        cfg = core.config.Config(shlex.split("-p test_module.foo=5"))
        module = TestModule(config=cfg)
        self.assertEqual(5, int(module.parameter("foo")))

    def test_default_parameter(self):
        cfg = core.config.Config([])
        module = TestModule(config=cfg)
        self.assertEqual("default", module.parameter("foo", "default"))

    def test_default_is_none(self):
        cfg = core.config.Config([])
        module = TestModule(config=cfg)
        self.assertEqual(None, module.parameter("foo"))

    def test_error_widget(self):
        cfg = core.config.Config([])
        module = TestModule(config=cfg)
        module.fail = True
        module.error = "!!"
        module.update_wrapper()
        self.assertEqual(1, len(module.widgets()))
        self.assertEqual("error: !!", module.widget().full_text())

    def test_get_widget_by_name(self):
        cfg = core.config.Config([])
        module = TestModule(config=cfg, widgets=[self.someWidget, self.anotherWidget])

        self.assertEqual(self.someWidget, module.widget(self.someWidget.name))
        self.assertEqual(self.anotherWidget, module.widget(self.anotherWidget.name))
        self.assertEqual(None, module.widget(self.unusedWidgetName))
        self.assertEqual(self.someWidget, module.widget())

    def test_default_thresholds(self):
        cfg = core.config.Config([])
        module = TestModule(config=cfg, widgets=[self.someWidget, self.anotherWidget])

        self.assertEqual("critical", module.threshold_state(100, 80, 99))
        self.assertEqual("warning", module.threshold_state(100, 80, 100))
        self.assertEqual("warning", module.threshold_state(81, 80, 100))
        self.assertEqual(None, module.threshold_state(80, 80, 100))
        self.assertEqual(None, module.threshold_state(10, 80, 100))

    def test_configured_callbacks(self):
        cfg = core.config.Config([])
        module = TestModule(config=cfg, widgets=[self.someWidget, self.anotherWidget])

        cmd = "sample-tool arg1 arg2 arg3"
        module.set("left-click", cmd)
        module.register_callbacks()

        with unittest.mock.patch("core.input.util.cli") as cli:
            cli.execute.return_value = ""
            core.input.trigger(
                {"button": core.input.LEFT_MOUSE, "instance": module.id,}
            )

            cli.execute.assert_called_once_with(cmd, wait=False, shell=True)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

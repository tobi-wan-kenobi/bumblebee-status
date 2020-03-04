import unittest

import shlex

import core.module
import core.widget
import core.config

class TestModule(core.module.Module):
    def update(self):
        if self.fail:
            raise Exception(self.error)
        pass

class module(unittest.TestCase):
    def setUp(self):
        self.invalidModuleName = 'invalid-module-name'
        self.validModuleName = 'test'
        self.someWidget = core.widget.Widget('randomeWidgetContent')
        self.anotherWidget = core.widget.Widget('more Widget content')

    def test_loadinvalid_module(self):
        config = unittest.mock.MagicMock()
        module = core.module.load(module_name=self.invalidModuleName, config=config)
        self.assertEqual('core.module', module.__class__.__module__, 'module must be a module object')
        self.assertEqual('Error', module.__class__.__name__, 'an invalid module must be a core.module.Error')

    def test_loadvalid_module(self):
        module = core.module.load(module_name=self.validModuleName)
        self.assertEqual('modules.{}'.format(self.validModuleName), module.__class__.__module__, 'module must be a modules.<name> object')
        self.assertEqual('Module', module.__class__.__name__, 'a valid module must have a Module class')
        self.assertEqual([], module.state(None), 'default state of module is empty')

    def test_empty_widgets(self):
        module = core.module.Module(widgets=[])
        self.assertEqual([], module.widgets())

    def test_error_widget(self):
        cfg = core.config.Config(shlex.split('-p test_module.foo=5'))
        module = core.module.Error(cfg, 'test-mod', 'xyz')
        self.assertEqual(['critical'], module.state(None), 'error module must have critical state')
        full_text = module.full_text(module.widget())
        self.assertTrue('test-mod' in full_text)
        self.assertTrue('xyz' in full_text)

    def test_single_widget(self):
        module = core.module.Module(widgets=self.someWidget)
        self.assertEqual([self.someWidget], module.widgets())

    def test_widget_list(self):
        module = core.module.Module(widgets=[ self.someWidget, self.anotherWidget ])
        self.assertEqual([ self.someWidget, self.anotherWidget ], module.widgets())

    def test_module_Name(self):
        module = TestModule()
        self.assertEqual('test_module', module.name(), 'module has wrong name')
        self.assertEqual('test_module', module.module_name(), 'module has wrong name')

    def testvalid_parameter(self):
        cfg = core.config.Config(shlex.split('-p test_module.foo=5'))
        module = TestModule(config=cfg)
        self.assertEqual(5, int(module.parameter('foo')))

    def test_default_parameter(self):
        cfg = core.config.Config([])
        module = TestModule(config=cfg)
        self.assertEqual('default', module.parameter('foo', 'default'))

    def test_default_is_none(self):
        cfg = core.config.Config([])
        module = TestModule(config=cfg)
        self.assertEqual(None, module.parameter('foo'))

    def test_error_widget(self):
        cfg = core.config.Config([])
        module = TestModule(config=cfg)
        module.fail = True
        module.error = '!!'
        module.update_wrapper()
        self.assertEqual(1, len(module.widgets()))
        self.assertEqual('error: !!', module.widget().full_text())

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

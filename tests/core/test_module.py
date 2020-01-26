import unittest

import core.module
import core.widget

class module(unittest.TestCase):
    def setUp(self):
        self._invalidModuleName = 'invalid-module-name'
        self._validModuleName = 'test'
        self.someWidget = core.widget.Widget('randomeWidgetContent')
        self.anotherWidget = core.widget.Widget('more Widget content')

    def tearDown(self):
        pass

    def test_load_invalid_module(self):
        module = core.module.load(self._invalidModuleName)
        self.assertEqual('core.module', module.__class__.__module__, 'module must be a module object')
        self.assertEqual('Error', module.__class__.__name__, 'an invalid module must be a core.module.Error')

    def test_load_valid_module(self):
        module = core.module.load(self._validModuleName)
        self.assertEqual('modules.{}'.format(self._validModuleName), module.__class__.__module__, 'module must be a modules.<name> object')
        self.assertEqual('Module', module.__class__.__name__, 'a valid module must have a Module class')

    def test_empty_widgets(self):
        module = core.module.Module(widgets=[])
        self.assertEqual([], module.widgets())

    def test_single_widget(self):
        module = core.module.Module(widgets=self.someWidget)
        self.assertEqual([self.someWidget], module.widgets())

    def test_widget_list(self):
        module = core.module.Module(widgets=[ self.someWidget, self.anotherWidget ])
        self.assertEqual([ self.someWidget, self.anotherWidget ], module.widgets())

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import unittest
import unittest.mock

import core.widget

class widget(unittest.TestCase):
    def setUp(self):
        self.someValue = 'some random value'
        self.someOtherValue = 'some different value'
        self.callbackReturnValue = 'callback return value'
        self.someWidget = core.widget.Widget(full_text=self.someValue)
        self.someCallback = unittest.mock.MagicMock(return_value=self.callbackReturnValue)

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

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

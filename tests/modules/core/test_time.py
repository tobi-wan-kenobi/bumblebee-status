import pytest
from unittest import TestCase, mock
from freezegun import freeze_time

import core.config
import core.input
import core.widget
import modules.core.time

pytest.importorskip("datetime")

def build_module(args = []):
    config = core.config.Config(args)
    return modules.core.time.Module(config=config, theme=None)

def build_widget():
    return core.widget.Widget()

class TimeTest(TestCase):
    def setup_class(self):
        locale_patcher = mock.patch('locale.getdefaultlocale')
        locale_mock = locale_patcher.start()
        locale_mock.return_value = ('en-US', 'UTF-8')

        self.widget = build_widget()

    def test_load_module(self):
        __import__("modules.core.time")

    @freeze_time('2020-10-15 03:25:59')
    def test_default_format(self):
        module = build_module()
        assert module.full_text(self.widget) == '03:25:59 AM'

    @freeze_time('2020-10-20 12:30:12')
    def test_custom_format(self):
        module = build_module(['-p', 'time.format=%H.%M.%S'])
        assert module.full_text(self.widget) == '12.30.12'

    @freeze_time('2020-01-10 10:20:30')
    @mock.patch('locale.getdefaultlocale')
    def test_invalid_locale(self, locale_mock):
        locale_mock.return_value = ('in-IN', 'UTF-0')

        module = build_module()
        assert module.full_text(self.widget) == '10:20:30 AM'

    @mock.patch('core.input.register')
    def test_register_left_mouse_action(self, input_register_mock):
        module = build_module()

        input_register_mock.assert_called_with(
            module,
            button=core.input.LEFT_MOUSE,
            cmd='calendar'
        )



import pytest
from unittest import TestCase, mock

import core.config
import core.widget
import modules.core.load

pytest.importorskip("os")
pytest.importorskip("multiprocessing")

def build_module():
    config = core.config.Config([])
    return modules.core.load.Module(config=config, theme=None)

def widget(module):
    return module.widgets()[0]

class TestLoad(TestCase):
    def test_load_module(self):
        __import__("modules.core.load")

    @mock.patch('multiprocessing.cpu_count')
    @mock.patch('os.getloadavg')
    def test_initial_values(self, load_avg_mock, cpu_count_mock):
        cpu_count_mock.return_value = 1
        load_avg_mock.return_value = (0.10, 0.20, 0.30)

        module = build_module()

        assert widget(module).full_text() == '0.00/0.00/0.00'

    @mock.patch('multiprocessing.cpu_count')
    @mock.patch('os.getloadavg')
    def test_update_values(self, load_avg_mock, cpu_count_mock):
        cpu_count_mock.return_value = 1
        load_avg_mock.return_value = (0.85, 0.95, 0.25)

        module = build_module()
        module.update()

        assert widget(module).full_text() == '0.85/0.95/0.25'

    @mock.patch('multiprocessing.cpu_count')
    @mock.patch('os.getloadavg')
    def test_cpu_count_exception(self, load_avg_mock, cpu_count_mock):
        cpu_count_mock.side_effect = NotImplementedError
        load_avg_mock.return_value = (0.1, 0.2, 0.3)

        module = build_module()
        module.update()

        assert widget(module).full_text() == '0.10/0.20/0.30'

    @mock.patch('multiprocessing.cpu_count')
    @mock.patch('os.getloadavg')
    def test_healthy_state(self, load_avg_mock, cpu_count_mock):
        cpu_count_mock.return_value = 1
        load_avg_mock.return_value = (0.55, 0.95, 0.25)

        module = build_module()
        module.update()

        assert module.state(widget(module)) == None

    @mock.patch('multiprocessing.cpu_count')
    @mock.patch('os.getloadavg')
    def test_warning_state(self, load_avg_mock, cpu_count_mock):
        cpu_count_mock.return_value = 1
        load_avg_mock.return_value = (0.8, 0.85, 0.9)

        module = build_module()
        module.update()

        assert module.state(widget(module)) == 'warning'

    @mock.patch('multiprocessing.cpu_count')
    @mock.patch('os.getloadavg')
    def test_critical_state(self, load_avg_mock, cpu_count_mock):
        cpu_count_mock.return_value = 1
        load_avg_mock.return_value = (0.95, 0.85, 0.9)

        module = build_module()
        module.update()

        assert module.state(widget(module)) == 'critical'

    @mock.patch('multiprocessing.cpu_count')
    @mock.patch('os.getloadavg')
    def test_healthy_state_with_8_cpus(self, load_avg_mock, cpu_count_mock):
        cpu_count_mock.return_value = 8
        load_avg_mock.return_value = (4.42, 0.85, 0.9)

        module = build_module()
        module.update()

        assert module.state(widget(module)) == None

    @mock.patch('multiprocessing.cpu_count')
    @mock.patch('os.getloadavg')
    def test_warning_state_with_8_cpus(self, load_avg_mock, cpu_count_mock):
        cpu_count_mock.return_value = 8
        load_avg_mock.return_value = (5.65, 0.85, 0.9)

        module = build_module()
        module.update()

        assert module.state(widget(module)) == 'warning'

    @mock.patch('multiprocessing.cpu_count')
    @mock.patch('os.getloadavg')
    def test_critical_state_with_8_cpus(self, load_avg_mock, cpu_count_mock):
        cpu_count_mock.return_value = 8
        load_avg_mock.return_value = (6.45, 0.85, 0.9)

        module = build_module()
        module.update()

        assert module.state(widget(module)) == 'critical'

    @mock.patch('multiprocessing.cpu_count')
    @mock.patch('os.getloadavg')
    @mock.patch('core.input.register')
    def test_register_left_mouse_action(self, input_register_mock, load_avg_mock, cpu_count_mock):
        module = build_module()

        input_register_mock.assert_called_with(
            module,
            button=core.input.LEFT_MOUSE,
            cmd='gnome-system-monitor'
        )


import pytest
from unittest import TestCase, mock

import core.config
import core.widget
import modules.core.cpu

pytest.importorskip("psutil")

def build_module(percpu=False):
    config = core.config.Config(["-p", "percpu={}".format(percpu)])
    config.set("cpu.percpu", percpu)
    return modules.core.cpu.Module(config=config, theme=None)

def cpu_widget(module):
    return module.widgets()[0]

class TestCPU(TestCase):
    def test_load_module(self):
        __import__("modules.core.cpu")

    @mock.patch('psutil.cpu_percent')
    def test_cpu_percent(self, cpu_percent_mock):
        cpu_percent_mock.return_value = 5
        module = build_module()

        assert cpu_widget(module).full_text() == '5.0%'

    @mock.patch('psutil.cpu_percent')
    def test_cpu_percent_update(self, cpu_percent_mock):
        cpu_percent_mock.return_value = 10
        module = build_module()

        assert cpu_widget(module).full_text() == '10.0%'

        cpu_percent_mock.return_value = 20
        module.update()

        assert cpu_widget(module).full_text() == '20.0%'

    @mock.patch('psutil.cpu_percent')
    def test_healthy_state(self, cpu_percent_mock):
        cpu_percent_mock.return_value = 50
        module = build_module()

        assert module.state(module.widget()) == None

    @mock.patch('psutil.cpu_percent')
    def test_warning_state(self, cpu_percent_mock):
        cpu_percent_mock.return_value = 75
        module = build_module()

        assert module.state(module.widget()) == 'warning'

    @mock.patch('psutil.cpu_percent')
    def test_critical_state(self, cpu_percent_mock):
        cpu_percent_mock.return_value = 82
        module = build_module()

        assert module.state(module.widget()) == 'critical'

    @mock.patch('psutil.cpu_percent')
    def test_healthy_state_percpu(self, cpu_percent_mock):
        cpu_percent_mock.return_value = [50,42,47]
        module = build_module(percpu=True)

        for widget in module.widgets():
            assert module.state(widget) == None

    @mock.patch('psutil.cpu_percent')
    def test_warning_state_percpu(self, cpu_percent_mock):
        cpu_percent_mock.return_value = [50,72,47]
        module = build_module(percpu=True)

        assert module.state(module.widgets()[0]) == None
        assert module.state(module.widgets()[1]) == "warning"
        assert module.state(module.widgets()[2]) == None

    @mock.patch('psutil.cpu_percent')
    def test_warning_state_percpu(self, cpu_percent_mock):
        cpu_percent_mock.return_value = [50,72,99]
        module = build_module(percpu=True)

        assert module.state(module.widgets()[0]) == None
        assert module.state(module.widgets()[1]) == "warning"
        assert module.state(module.widgets()[2]) == "critical" 

    @mock.patch('core.input.register')
    def test_register_left_mouse_action(self, input_register_mock):
        module = build_module()

        input_register_mock.assert_called_with(
            module,
            button=core.input.LEFT_MOUSE,
            cmd='gnome-system-monitor'
        )



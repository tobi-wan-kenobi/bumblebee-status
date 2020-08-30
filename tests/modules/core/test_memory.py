import pytest
from unittest import TestCase, mock

import core.config
import core.widget
import modules.core.memory

def build_module(args = []):
    config = core.config.Config(args)
    return modules.core.memory.Module(config=config, theme=None)

def memory_widget(module):
    return module.widgets()[0]

def meminfo_mock(
    total,
    available,
    unit = 'kB',
    free = 0,
    buffers = 0,
    cached = 0,
    slab = 0
):
    data = []
    states = [
        ('MemTotal', total),
        ('MemAvailable', available),
        ('MemFree', free),
        ('Buffers', buffers),
        ('Cached', cached),
        ('Slab', slab)
    ]

    for i, (key, value) in enumerate(states):
        data.append('{}: {} {}'.format(key, value, unit))

    return '\n'.join(data)

class TestMemory(TestCase):
    def test_load_module(self):
        __import__("modules.core.memory")

    @mock.patch('builtins.open', mock.mock_open(read_data=meminfo_mock(2048, 1024)))
    def test_default_healthy_state(self):
        module = build_module()
        module.update()

        widget = memory_widget(module)

        assert widget.full_text() == '1.00MiB/2.00MiB (50.00%)'
        assert module.state(widget) == None

    @mock.patch('builtins.open', mock.mock_open(read_data=meminfo_mock(8196, 1024)))
    def test_default_warning_state(self):
        module = build_module()
        module.update()

        widget = memory_widget(module)

        assert widget.full_text() == '7.00MiB/8.00MiB (87.51%)'
        assert module.state(widget) == 'warning'

    @mock.patch('builtins.open', mock.mock_open(read_data=meminfo_mock(2048, 0)))
    def test_default_critical_state(self):
        module = build_module()
        module.update()

        widget = memory_widget(module)

        assert widget.full_text() == '2.00MiB/2.00MiB (100.00%)'
        assert module.state(widget) == 'critical'

    @mock.patch('builtins.open', mock.mock_open(read_data=meminfo_mock(4096, 3068)))
    def test_custom_warning_parameter(self):
        module = build_module(['-p', 'memory.warning=20'])
        module.update()

        widget = memory_widget(module)

        assert widget.full_text() == '1.00MiB/4.00MiB (25.10%)'
        assert module.state(widget) == 'warning'

    @mock.patch('builtins.open', mock.mock_open(read_data=meminfo_mock(8196, 4096)))
    def test_custom_critical_parameter(self):
        module = build_module(['-p', 'memory.critical=50'])
        module.update()

        widget = memory_widget(module)

        assert widget.full_text() == '4.00MiB/8.00MiB (50.02%)'
        assert module.state(widget) == 'critical'

    @mock.patch('builtins.open', mock.mock_open(read_data=meminfo_mock(2048, 1024)))
    def test_usedonly_parameter(self):
        module = build_module(['-p', 'memory.usedonly=true'])
        module.update()

        widget = memory_widget(module)

        assert widget.full_text() == '1.00MiB'
        assert module.state(widget) == None

    @mock.patch('builtins.open', mock.mock_open(read_data=meminfo_mock(2048, 1024)))
    def test_format_parameter(self):
        module = build_module(['-p', 'memory.format={used}.{total}'])
        module.update()

        widget = memory_widget(module)

        assert widget.full_text() == '1.00MiB.2.00MiB'
        assert module.state(widget) == None

    @mock.patch('builtins.open', mock.mock_open(read_data=meminfo_mock(2048, 1024)))
    def test_format_parameter_with_percent(self):
        module = build_module(['-p', 'memory.format={percent}%'])
        module.update()

        widget = memory_widget(module)

        assert widget.full_text() == '50.0%'
        assert module.state(widget) == None


    @mock.patch('builtins.open', mock.mock_open(read_data=meminfo_mock(8196, 4096, 'mB')))
    def test_mb_unit(self):
        module = build_module()
        module.update()

        widget = memory_widget(module)

        assert widget.full_text() == '4.00GiB/8.00GiB (50.02%)'
        assert module.state(widget) == None

    @mock.patch('builtins.open', mock.mock_open(read_data=meminfo_mock(2, 1, 'gB')))
    def test_gb_unit(self):
        module = build_module()
        module.update()

        widget = memory_widget(module)

        assert widget.full_text() == '1.00GiB/2.00GiB (50.00%)'
        assert module.state(widget) == None


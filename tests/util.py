# pylint: disable=C0103,C0111,W0613

import json
import shlex
import subprocess

from bumblebee.output import Widget

def assertWidgetAttributes(test, widget):
    test.assertTrue(isinstance(widget, Widget))
    test.assertTrue(hasattr(widget, "full_text"))

def assertPopen(output, cmd):
    res = shlex.split(cmd)
    output.assert_any_call(res,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )

def assertStateContains(test, module, state):
    for widget in module.widgets():
        widget.link_module(module)
    module.update(module.widgets())
    test.assertTrue(state in module.widgets()[0].state())

class MockEpoll(object):
    def register(self, fileno, event):
        pass

    def poll(self, timeout):
        return [(1,2)]

    def unregister(self, fileno):
        pass

    def close(self):
        pass

def assertMouseEvent(mock_input, mock_output, mock_select, engine, module, button, cmd, instance_id=None):
        mock_input.readline.return_value = json.dumps({
            "name": module.id if module else "test",
            "button": button,
            "instance": instance_id
        })
        mock_input.fileno.return_value = 1
        mock_select.return_value = MockEpoll()
        engine.input.start()
        engine.input.stop()
        mock_input.readline.assert_any_call()
        if cmd:
            assertPopen(mock_output, cmd)

class MockInput(object):
    def __init__(self):
        self._callbacks = {}
    def start(self):
        pass

    def stop(self):
        pass

    def get_callback(self, uid):
        return self._callbacks.get(uid, None)

    def register_callback(self, obj, button, cmd):
        if not obj:
            return
        self._callbacks[obj.id] = {
            "button": button,
            "command": cmd,
        }

class MockEngine(object):
    def __init__(self):
        self.input = MockInput()

class MockConfig(object):
    def __init__(self):
        self._data = {}

    def get(self, name, default):
        if name in self._data:
            return self._data[name]
        return default

    def set(self, name, value):
        self._data[name] = value

class MockOutput(object):
    def start(self):
        pass

    def stop(self):
        pass

    def draw(self, widget, engine, module):
        engine.stop()

    def begin(self):
        pass

    def flush(self):
        pass

    def end(self):
        pass

class MockModule(object):
    def __init__(self, engine=None, config=None):
        self.id = None

class MockWidget(Widget):
    def __init__(self, text):
        super(MockWidget, self).__init__(text)
        self._text = text
        self.module = None
        self.attr_state = ["state-default"]
        self.id = "none"

    def state(self):
        return self.attr_state

    def update(self, widgets):
        pass

    def full_text(self):
        return self._text

class MockTheme(object):
    def __init__(self):
        self.attr_prefix = None
        self.attr_suffix = None
        self.attr_fg = None
        self.attr_bg = None
        self.attr_separator = None
        self.attr_separator_block_width = 0

    def padding(self, widget):
        return ""

    def reset(self):
        pass

    def separator_block_width(self, widget):
        return self.attr_separator_block_width

    def separator(self, widget):
        return self.attr_separator

    def prefix(self, widget, default=None):
        return self.attr_prefix

    def suffix(self, widget, default=None):
        return self.attr_suffix

    def fg(self, widget):
        return self.attr_fg

    def bg(self, widget):
        return self.attr_bg

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# pylint: disable=C0103,C0111

import mock
import json
import shlex
import subprocess

from bumblebee.output import Widget

import random, string

def rand(cnt):
    return "".join(random.choice(string.lowercase) for i in range(cnt))

def mouseEvent(stdin, button, inp, module=None, instance=None):
    stdin.readline.return_value = json.dumps({
        "name": module.id if module else rand(10),
        "button": button,
        "instance": instance
    })
    inp.start()
    inp.stop()
    stdin.readline.assert_any_call()

class MockPopen(object):
    def __init__(self, module=""):
        if len(module) > 0: module = "{}.".format(module)
        self._patch = mock.patch("{}subprocess.Popen".format(module))
        self._popen = self._patch.start()
        self.mock = mock.Mock()
        # for a nicer, more uniform interface
        self.mock.popen = self._popen
        # for easier command execution checks
        self.mock.popen.assert_call = self.assert_call
        self._popen.return_value = self.mock

        self.mock.communicate.return_value = [ "", None ]
        self.mock.returncode = 0

    def assert_call(self, cmd):
        self.mock.popen.assert_called_with(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def cleanup(self):
        self._patch.stop()

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

class MockEngine(object):
    def __init__(self):
        self.input = MockInput()

class MockWidget(Widget):
    def __init__(self, text):
        super(MockWidget, self).__init__(text)
        self.module = None
        self.attr_state = ["state-default"]
        self.id = rand(10)

        self.full_text(text)

#    def state(self):
#        return self.attr_state

    def update(self, widgets):
        pass

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

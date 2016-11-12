import os
import shlex
import inspect
import threading
import subprocess

def output(args):
    import bumblebee.outputs.i3
    return bumblebee.outputs.i3.Output(args)

class Widget(object):
    def __init__(self, obj, text):
        self._obj = obj
        self._text = text
        self._store = {}

    def set(self, key, value):
        self._store[key] = value

    def get(self, key, default=None):
        return self._store.get(key, default)

    def state(self):
        return self._obj.state(self)

    def warning(self):
        return self._obj.warning(self)

    def critical(self):
        return self._obj.critical(self)

    def module(self):
        return self._obj.__module__.split(".")[-1]

    def instance(self):
        return getattr(self._obj, "instance")(self)

    def text(self):
        return self._text

class Command(object):
    def __init__(self, command):
        self._command = command

    def __call__(self, *args, **kwargs):
        cmd = self._command.format(*args, **kwargs)
        DEVNULL = open(os.devnull, 'wb')
        subprocess.Popen(shlex.split(cmd), stdout=DEVNULL, stderr=DEVNULL)

class Output(object):
    def __init__(self, config):
        self._config = config
        self._callbacks = {}
        self._wait = threading.Condition()
        self._wait.acquire()

    def redraw(self):
        self._wait.acquire()
        self._wait.notify()
        self._wait.release()

    def add_callback(self, cmd, button, module=None):
        if module:
            module = module.replace("bumblebee.modules.", "")

        if self._callbacks.get((button, module)): return

        self._callbacks[(
            button,
            module,
        )] = cmd

    def callback(self, event):
        cb = self._callbacks.get((
            event.get("button", -1),
            None,
        ), None)
        cb = self._callbacks.get((
            event.get("button", -1),
            event.get("instance", event.get("name", None)),
        ), cb)
        if inspect.isfunction(cb) or cb is None: return cb

        return Command(cb)

    def wait(self):
        self._wait.wait(self._config.parameter("interval", 1))

    def start(self):
        pass

    def draw(self, widgets, theme):
        if not type(widgets) is list:
            widgets = [ widgets ]
        self._draw(widgets, theme)

    def _draw(self, widgets, theme):
        pass

    def flush(self):
        pass

    def stop(self):
        pass

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

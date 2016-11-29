import os
import shlex
import inspect
import threading
import subprocess

def output(args):
    import bumblebee.outputs.i3
    return bumblebee.outputs.i3.Output(args)

class Widget(object):
    def __init__(self, obj, text, instance=None):
        self._obj = obj
        self._text = text
        self._store = {}
        self._instance = instance

        obj._output.register_widget(self.instance(), self)

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
        return self._instance if self._instance else getattr(self._obj, "instance")(self)

    def text(self):
        return self._text

class Command(object):
    def __init__(self, command, event, widget):
        self._command = command
        self._event = event
        self._widget = widget

    def __call__(self, *args, **kwargs):
        if not isinstance(self._command, list):
            self._command = [ self._command ]

        for cmd in self._command:
            if not cmd: continue
            if inspect.ismethod(cmd):
                cmd(self._event, self._widget)
            else:
                c = cmd.format(*args, **kwargs)
                DEVNULL = open(os.devnull, 'wb')
                subprocess.Popen(shlex.split(c), stdout=DEVNULL, stderr=DEVNULL)

class Output(object):
    def __init__(self, config):
        self._config = config
        self._callbacks = {}
        self._wait = threading.Condition()
        self._wait.acquire()
        self._widgets = {}

    def register_widget(self, identity, widget):
        self._widgets[identity] = widget

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
            event.get("instance", event.get("module", None)),
        ), cb)

        identity = event.get("instance", event.get("module", None))
        return Command(cb, event, self._widgets.get(identity, None))

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

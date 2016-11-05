import inspect
import threading

def output(args):
    import bumblebee.outputs.i3
    return bumblebee.outputs.i3.Output(args)

class Widget(object):
    def __init__(self, text, warning=False, critical=False, state=None):
        self._name = inspect.getmodule(inspect.stack()[1][0]).__name__
        self._text = text
        self._warning = warning
        self._critical = critical
        self._state = state

    def state(self):
        return self._state

    def warning(self):
        return self._warning

    def critical(self):
        return self._critical

    def module(self):
        return self._name.split(".")[-1]

    def name(self):
        return self._name

    def text(self):
        return self._text

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
        self._callbacks[(
            button,
            module,
        )] = cmd

    def callback(self, event):
        cb = self._callbacks.get((
            event.get("button", -1),
            event.get("name", None),
        ), None)
        if cb is not None: return cb
        cb = self._callbacks.get((
            event.get("button", -1),
            None,
        ), None)
        return cb

    def wait(self):
        self._wait.wait(self._config.parameter("interval", 1))

    def start(self):
        pass

    def draw(self, widgets, theme):
        pass

    def flush(self):
        pass

    def stop(self):
        pass

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

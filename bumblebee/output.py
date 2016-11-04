import threading

def output(args):
    import bumblebee.outputs.i3
    return bumblebee.outputs.i3.Output(args)

class Output(object):
    def __init__(self, args):
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

    def wait(self, interval):
        self._wait.wait(interval)

    def start(self):
        pass

    def add(self, obj, theme):
        pass

    def get(self):
        pass

    def stop(self):
        pass

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

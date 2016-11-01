
class Output(object):
    def __init__(self, theme):
        self._theme = theme
        self._callbacks = {}

    def add_callback(self, cmd, button, module=None, instance=None):
        self._callbacks[(
            button,
            module,
            instance
        )] = cmd

    def callback(self, event):
        cb = self._callbacks.get((
            event.get("button", -1),
            event.get("name", None),
            event.get("instance", None)
        ), None)
        if cb is not None: return cb
        cb = self._callbacks.get((
            event.get("button", -1),
            event.get("name", None),
            None
        ), None)
        if cb is not None: return cb
        cb = self._callbacks.get((
            event.get("button", -1),
            None,
            None
        ), None)
        return cb

    def theme(self):
        return self._theme

    def start(self):
        pass

    def add(self, obj):
        pass

    def get(self):
        pass

    def stop(self):
        pass

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

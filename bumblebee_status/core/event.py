__callbacks = {}


def register(event, callback, *args, **kwargs):
    cb = callback
    if args or kwargs:
        cb = lambda: callback(*args, **kwargs)

    __callbacks.setdefault(event, []).append(cb)

def register_exclusive(event, callback, *args, **kwargs):
    cb = callback
    if args or kwargs:
        cb = lambda: callback(*args, **kwargs)

    __callbacks[event] = [cb]

def unregister(event):
    if event in __callbacks:
        del __callbacks[event]

def clear():
    __callbacks.clear()


def trigger(event, *args, **kwargs):
    cb = __callbacks.get(event, [])
    if len(cb) == 0:
        return False

    for callback in cb:
        if args or kwargs:
            callback(*args, **kwargs)
        else:
            callback()
    return True


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

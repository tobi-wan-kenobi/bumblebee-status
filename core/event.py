__callbacks = {}


def register(event, callback, *args, **kwargs):
    cb = callback
    if len(args) + len(kwargs) > 0:
        cb = lambda: callback(*args, **kwargs)

    __callbacks.setdefault(event, []).append(cb)


def clear():
    __callbacks.clear()


def trigger(event, *args, **kwargs):
    cb = __callbacks.get(event, [])
    if len(cb) == 0:
        return False

    for callback in cb:
        if len(args) + len(kwargs) == 0:
            callback()
        else:
            callback(*args, **kwargs)
    return True


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

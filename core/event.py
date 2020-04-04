
__callbacks = {}

def register(event, callback, *args, **kwargs):
    cb = callback
    if len(args) + len(kwargs) > 0:
        print("registering lambda: {} {}".format(len(args), len(kwargs)))
        cb = lambda: callback(*args, **kwargs)

    __callbacks.setdefault(event, []).append(cb)

def clear():
    __callbacks.clear()

def trigger(event, *args, **kwargs):
    for callback in __callbacks.get(event, []):
        if len(args) + len(kwargs) == 0:
            callback()
        else:
            callback(*args, **kwargs)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

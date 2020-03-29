
__callbacks = {}

def register(event, callback, *args, **kwargs):
    __callbacks.setdefault(event, []).append(
        lambda: callback(*args, **kwargs)
    )

def clear():
    __callbacks.clear()

def trigger(event):
    for callback in __callbacks.get(event, []):
        callback()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

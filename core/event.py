
callbacks = {}

def register(event, callback, *args, **kwargs):
    callbacks.setdefault(event, []).append(
        lambda: callback(*args, **kwargs)
    )

def trigger(event):
    for callback in callbacks.get(event, []):
        callback()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

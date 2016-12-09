"""Store interface

Allows arbitrary classes to offer a simple get/set
store interface by deriving from the Store class in
this module
"""

class Store(object):
    def __init__(self):
        self._data = {}

    def set(self, key, value):
        self._data[key] = value

    def get(self, key, default=None):
        return self._data.get(key, default)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

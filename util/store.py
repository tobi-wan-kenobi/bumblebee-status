"""Store interface

Allows arbitrary classes to offer a simple get/set
store interface by deriving from the Store class in
this module
"""


class Store(object):
    """Interface for storing and retrieving simple values"""

    def __init__(self):
        super(Store, self).__init__()
        self._data = {}

    def set(self, key, value):
        """Sets key to value, overwriting any existing data for that key

        :param key: the name of the parameter to set
        :param value: the value to be set
        """
        self._data[key] = {"value": value, "used": False}

    def unused_keys(self):
        """Returns a list of unused keys

        :return: a list of keys that are set, but never used
        :rtype: list of strings
        """
        return [key for key, value in self._data.items() if value["used"] == False]

    def get(self, key, default=None):
        """Returns the current value for the specified key, or a default value,
        if the key is not set

        :param key: the name of the parameter to retrieve
        :param default: the default value to return, defaults to None
        """
        if key in self._data:
            self._data[key]["used"] = True
        return self._data.get(key, {"value": default})["value"]


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

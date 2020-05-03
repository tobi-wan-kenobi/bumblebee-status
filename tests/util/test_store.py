import unittest

import util.store


class store(unittest.TestCase):
    def setUp(self):
        self.store = util.store.Store()

        self.unusedKey = "someRandomUnusedKey"
        self.someKey = "someRandomKey"
        self.someOtherKey = "anotherRandomKey"
        self.someValue = "someRandomValue"
        self.someOtherValue = "anotherRandomValue"

    def test_get_of_unset_key(self):
        self.assertEqual(
            None, self.store.get(self.unusedKey), "default value expected to be None"
        )
        self.assertEqual(
            self.someValue,
            self.store.get(self.unusedKey, self.someValue),
            "wrong user-provided default value returned",
        )

    def test_get_of_set_key(self):
        self.assertNotEqual(self.someValue, None)

        self.store.set(self.someKey, self.someValue)
        self.assertEqual(
            self.someValue,
            self.store.get(self.someKey),
            "unexpected value for existing key",
        )

    def test_overwrite_set(self):
        self.assertNotEqual(self.someValue, None)
        self.assertNotEqual(self.someOtherValue, self.someValue)

        self.store.set(self.someKey, self.someValue)
        self.store.set(self.someKey, self.someOtherValue)
        self.assertEqual(
            self.someOtherValue,
            self.store.get(self.someKey),
            "unexpected value for existing key",
        )

    def test_unused_keys(self):
        self.assertNotEqual(self.someKey, self.someOtherKey)

        self.store.set(self.someKey, self.someValue)
        self.store.set(self.someOtherKey, self.someOtherValue)

        self.assertEqual(
            sorted(self.store.unused_keys()), sorted([self.someKey, self.someOtherKey])
        )

        self.store.get(self.someKey)
        self.assertEqual(self.store.unused_keys(), [self.someOtherKey])


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import unittest

from util.algorithm import *


class algorithm(unittest.TestCase):
    def setUp(self):
        self.someData = {"a": 100, "b": 200, "c": [1, 2, 3]}
        self.differentData = {"x": 20, "y": "bla", "z": ["a", "b"]}
        self.moreData = {"n": 100}
        self.overlapData = {"a": 200, "c": [1, 2, 4]}

    def test_merge_with_empty(self):
        self.assertEqual(self.someData, merge(self.someData, {}))
        self.assertEqual(None, merge(self.someData, None))

    def test_merge_no_overwrite(self):
        result = merge(self.someData, self.differentData)
        for k in self.someData:
            self.assertEqual(result[k], self.someData[k])
        for k in self.differentData:
            self.assertEqual(result[k], self.differentData[k])

    def test_merge_multiple(self):
        result = merge(self.someData, self.differentData, self.moreData)
        for k in self.someData:
            self.assertEqual(result[k], self.someData[k])
        for k in self.differentData:
            self.assertEqual(result[k], self.differentData[k])
        for k in self.moreData:
            self.assertEqual(result[k], self.moreData[k])

    def merge_overlap(self):
        result = merge(self.someData, self.overlapData)
        for k in self.someData:
            if not k in self.overlapData:
                self.assertEqual(result[k], self.someData[k])
        for k in self.overlapData:
            self.assertEqual(result[k], self.overlapData[k])


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

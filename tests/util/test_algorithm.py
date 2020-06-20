import pytest

from util.algorithm import *


@pytest.fixture
def someData():
    return {"a": 100, "b": 200, "c": [1, 2, 3]}


@pytest.fixture
def differentData():
    return {"x": 20, "y": "bla", "z": ["a", "b"]}


@pytest.fixture
def moreData():
    return {"n": 100}


@pytest.fixture
def overlapData():
    return {"a": 200, "c": [1, 2, 4]}


def test_merge_with_empty(someData):
    assert merge(someData, {}) == someData
    assert merge(someData, None) == None

    def test_merge_no_overwrite(someData, differentData):
        result = merge(someData, differentData)
        for k in someData:
            assert someData[k] == result[k]
        for k in self.differentData:
            assert differentData[k] == result[k]

    def test_merge_multiple(someData, differentData, moreData):
        result = merge(someData, differentData, moreData)
        for k in someData:
            assert someData[k] == result[k]
        for k in differentData:
            assert differentData[k] == result[k]
        for k in moreData:
            assert moreData[k] == result[k]

    def merge_overlap(someData, overlapData):
        result = merge(someData, overlapData)
        for k in someData:
            if not k in self.overlapData:
                assert someData[k] == result[k]
        for k in self.overlapData:
            assert overlapData[k] == result[k]


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

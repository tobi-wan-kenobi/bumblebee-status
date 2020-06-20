import pytest

import util.store


@pytest.fixture
def emptyStore():
    return util.store.Store()


@pytest.fixture
def store():
    return util.store.Store()


def test_get_of_unset_key(emptyStore):
    assert emptyStore.get("any-key") == None
    assert emptyStore.get("any-key", "default-value") == "default-value"


def test_get_of_set_key(store):
    store.set("key", "value")
    assert store.get("key") == "value"


def test_overwrite_set(store):
    store.set("key", "value 1")
    store.set("key", "value 2")

    assert store.get("key") == "value 2"


def test_unused_keys(store):
    store.set("key 1", "value x")
    store.set("key 2", "value y")

    assert sorted(store.unused_keys()) == sorted(["key 1", "key 2"])

    store.get("key 2")

    assert store.unused_keys() == ["key 1"]

    store.get("key 1")

    assert store.unused_keys() == []


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

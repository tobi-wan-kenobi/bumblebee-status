import util.store


def test_get_returns_set_value():
    s = util.store.Store()
    s.set("key", "value")
    assert s.get("key") == "value"


def test_get_returns_default_for_missing_key():
    s = util.store.Store()
    assert s.get("missing") is None
    assert s.get("missing", "default") == "default"


def test_get_does_not_mutate_internal_used_flag():
    s = util.store.Store()
    s.set("key", "value")
    s.get("key")
    # After the fix, 'used' stays False (tracking removed from hot path)
    assert s._data["key"]["used"] == False


def test_overwrite_set():
    s = util.store.Store()
    s.set("key", "value 1")
    s.set("key", "value 2")
    assert s.get("key") == "value 2"


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

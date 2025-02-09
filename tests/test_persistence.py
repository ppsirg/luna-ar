import pytest


def test_add(data_storage):
    resp = data_storage.add("key1", {"a": 1, "b": 2})
    assert resp, "not succeded insertion"
    saved = data_storage.get("key1")
    assert saved is not None, "data not found"


def test_delete(data_storage):
    data_storage.add("key2", {"c": 3, "d": 4})
    data_storage.delete("key2")
    saved = data_storage.get("key2")
    assert saved is None, "info not deleted"


def test_update(data_storage):
    data_storage.add("key3", {"e": 5, "f": 6})
    data_storage.update("key3", {"g": 7})
    saved = data_storage.get("key3")
    assert saved == {"g": 7}


def test_list(data_storage):
    data_storage.add("key4", {"h": 8, "i": 9})
    data_storage.add("key5", {"h": 8, "i": 9})
    data = data_storage.list()
    assert len(data) == 2, "incomplete data"
    assert all(
        (i in (a["key"] for a in data) for i in ("key4", "key5"))
    ), "incomplete keys"
    # assert [a['value'] for a in data] == ['key4', 'key5']

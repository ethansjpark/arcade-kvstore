import pytest
from app.store import Store

def test_basic_set_get():
    s = Store()
    s.set("a", 1)
    assert s.get("a") == 1

def test_delete_removes_key():
    s = Store()
    s.set("a", 1)
    s.delete("a")
    assert s.get("a") is None

def test_commit_persists_changes():
    s = Store()
    s.begin()
    s.set("a", 42)
    assert s.get("a") == 42  # visible inside txn
    s.commit()
    assert s.get("a") == 42  # visible after commit

def test_rollback_discards_changes():
    s = Store()
    s.begin()
    s.set("a", 99)
    s.rollback()
    assert s.get("a") is None

def test_nested_transactions():
    s = Store()
    s.set("x", "base")
    s.begin()
    s.set("x", "tx1")
    s.begin()
    s.set("x", "tx2")
    assert s.get("x") == "tx2"
    s.commit()    # merge tx2 into tx1
    assert s.get("x") == "tx2"
    s.rollback()  # discard tx1
    assert s.get("x") == "base"

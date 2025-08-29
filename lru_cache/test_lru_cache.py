import pytest
from lru_cache import LruCache  # dostosuj import do swojej ścieżki

def test_capacity_must_be_positive():
    with pytest.raises(ValueError):
        LruCache(0)

def test_basic_put_get_and_len():
    c = LruCache(2)
    c.put("a", 1)
    c.put("b", 2)
    assert len(c) == 2
    assert c.get("a") == 1
    assert c.get("b") == 2

def test_get_refreshes_recency_fifo_eviction():
    c = LruCache(2)
    c.put("a", 1)
    c.put("b", 2)
    # odśwież 'a' -> staje się najświeższe
    assert c.get("a") == 1
    # dodanie 'c' wyrzuca najstarsze (czyli 'b')
    c.put("c", 3)
    assert c.get("b") is None
    assert c.get("a") == 1
    assert c.get("c") == 3

def test_put_existing_updates_and_refreshes():
    c = LruCache(2)
    c.put("a", 1)
    c.put("b", 2)
    c.put("a", 10)  # update + odśwież
    c.put("c", 3)   # powinno wyrzucić 'b'
    assert c.get("b") is None
    assert c.get("a") == 10
    assert c.get("c") == 3
    assert len(c) == 2

@pytest.mark.parametrize(
    "ops,expected",
    ids=["simple_chain","update_then_eviction"],
    argvalues=[
        (
            [("put","x",1),("put","y",2),("put","z",3),("get","x"),("get","y"),("get","z")],
            [None,None,None,None,2,3]
        ),
        (
            [("put","k",1),("put","m",2),("put","k",5),("put","n",3),("get","m"),("get","k"),("get","n")],
            [None,None,None,None,None,5,3]
        ),
    ],
)
def test_scenario_table(ops, expected):
    c = LruCache(2)
    out = []
    for op in ops:
        if op[0] == "put":
            _, k, v = op
            c.put(k, v)
            out.append(None)  # None
        elif op[0] == "get":
            _, k = op
            out.append(c.get(k))
    assert out == expected

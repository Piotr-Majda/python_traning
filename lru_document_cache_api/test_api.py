import pytest

from fastapi.testclient import TestClient
from lru_document_cache_api.api import app


@pytest.fixture(scope='function')
def client():
    return TestClient(app)


def test_put_user_settings_capacity(client):
    r = client.put('/users/u1/settings', json={'capacity': '2'})
    assert r.status_code == 200
    assert r.json() == {'size': 0}

def test_capacity_shrink_evicts_lru(client):
    # ustaw pojemność 3
    r = client.put('/users/u1/settings', json={'capacity': 3})
    assert r.status_code == 200
    assert r.json() == {'size': 0}

    # dodaj 3 dokumenty: a (LRU), b, c (MRU)
    assert client.post('/users/u1/cache', json={'doc_id': 'a', 'content': 'A'}).status_code in (200, 201)
    assert client.post('/users/u1/cache', json={'doc_id': 'b', 'content': 'B'}).status_code in (200, 201)
    assert client.post('/users/u1/cache', json={'doc_id': 'c', 'content': 'C'}).status_code in (200, 201)

    # lista MRU (oczekiwana kolejność: c, b, a)
    r = client.get('/users/u1/cache')  # domyślnie order = "mru"
    assert r.status_code == 200
    body = r.json()
    # oczekujemy co najmniej: {"items":[{"doc_id":...}, ...], "size":3}
    assert body["size"] == 3
    assert [item["doc_id"] for item in body["items"]] == ["c", "b", "a"]

    # przytnij capacity do 2 -> ma wylecieć LRU = "a"
    r = client.put('/users/u1/settings', json={'capacity': 2})
    assert r.status_code == 200
    assert r.json() == {'size': 2}  # rozmiar PO przycięciu

    # a zostało wyparte
    r = client.get('/users/u1/cache/a')
    assert r.status_code == 404

    # lista MRU po przycięciu: ["c", "b"]
    r = client.get('/users/u1/cache')
    assert r.status_code == 200
    body = r.json()
    assert body["size"] == 2
    assert [item["doc_id"] for item in body["items"]] == ["c", "b"]


def test_get_promotes_to_mru_and_post_update_does_not_increase_size(client):
    # capacity = 3
    r = client.put('/users/u1/settings', json={'capacity': 3})
    assert r.status_code == 200
    assert r.json() == {'size': 0}

    # dodaj a, b, c (MRU kolejno: c,b,a)
    assert client.post('/users/u1/cache', json={'doc_id':'a','content':'A'}).status_code in (200,201)
    assert client.post('/users/u1/cache', json={'doc_id':'b','content':'B'}).status_code in (200,201)
    assert client.post('/users/u1/cache', json={'doc_id':'c','content':'C'}).status_code in (200,201)

    # lista MRU: c, b, a
    r = client.get('/users/u1/cache')
    assert r.status_code == 200
    body = r.json()
    assert body["size"] == 3
    assert [i["doc_id"] for i in body["items"]] == ["c","b","a"]

    # GET b -> b staje się MRU: b, c, a
    r = client.get('/users/u1/cache/b')
    assert r.status_code == 200

    r = client.get('/users/u1/cache')
    body = r.json()
    assert [i["doc_id"] for i in body["items"]] == ["b","c","a"]

    # POST istniejącego 'c' (aktualizacja content) -> size nie rośnie, c staje się MRU: c, b, a
    before_size = body["size"]
    r = client.post('/users/u1/cache', json={'doc_id':'c','content':'C2'})
    assert r.status_code in (200,201)  # możesz zwrócić 200 za update

    r = client.get('/users/u1/cache')
    body2 = r.json()
    assert body2["size"] == before_size  # brak wzrostu rozmiaru
    assert [i["doc_id"] for i in body2["items"]] == ["c","b","a"]

    # GET c -> updated_at powinno się zmienić między pierwszym a drugim odczytem
    r1 = client.get('/users/u1/cache/c')
    t1 = r1.json()["updated_at"]
    r2 = client.get('/users/u1/cache/c')
    t2 = r2.json()["updated_at"]
    assert t2 >= t1  # dopuszczamy równe, jeśli nie odświeżasz przy GET; lepiej żeby rosło

def test_post_new_evicts_lru(client):
    # capacity = 2
    r = client.put('/users/u1/settings', json={'capacity': 2})
    assert r.status_code == 200
    assert r.json() == {'size': 0}

    # a (MRU=a), b (MRU=b, LRU=a)
    assert client.post('/users/u1/cache', json={'doc_id':'a','content':'A'}).status_code in (200,201)
    assert client.post('/users/u1/cache', json={'doc_id':'b','content':'B'}).status_code in (200,201)

    # wstaw c -> powinno wyrzucić LRU=a; MRU kolejnosć: c, b
    assert client.post('/users/u1/cache', json={'doc_id':'c','content':'C'}).status_code in (200,201)

    r = client.get('/users/u1/cache')
    assert r.status_code == 200
    body = r.json()
    assert body["size"] == 2
    assert [i["doc_id"] for i in body["items"]] == ["c","b"]

    # a nie istnieje
    r = client.get('/users/u1/cache/a')
    assert r.status_code == 404

def test_update_no_size_increase_and_order(client):
    r = client.put('/users/u1/settings', json={'capacity': 2})
    assert r.status_code == 200

    # a (MRU=a), b (MRU=b, LRU=a)
    assert client.post('/users/u1/cache', json={'doc_id':'a','content':'A'}).status_code in (200,201)
    assert client.post('/users/u1/cache', json={'doc_id':'b','content':'B'}).status_code in (200,201)

    # update a -> a staje się MRU: [a, b], size nadal 2
    r = client.post('/users/u1/cache', json={'doc_id':'a','content':'A2'})
    assert r.status_code in (200,201)

    r = client.get('/users/u1/cache')
    body = r.json()
    assert body["size"] == 2
    assert [i["doc_id"] for i in body["items"]] == ["a","b"]

    # teraz POST c powinno wyrzucić LRU=b (bo po update a: LRU=b)
    assert client.post('/users/u1/cache', json={'doc_id':'c','content':'C'}).status_code in (200,201)
    r = client.get('/users/u1/cache')
    body = r.json()
    assert body["size"] == 2
    assert [i["doc_id"] for i in body["items"]] == ["c","a"]
    assert client.get('/users/u1/cache/b').status_code == 404

def test_get_promote_changes_next_eviction(client):
    r = client.put('/users/u1/settings', json={'capacity': 2})
    assert r.status_code == 200

    # a (MRU=a), b (MRU=b, LRU=a)
    assert client.post('/users/u1/cache', json={'doc_id':'a','content':'A'}).status_code in (200,201)
    assert client.post('/users/u1/cache', json={'doc_id':'b','content':'B'}).status_code in (200,201)

    # GET a -> a promowany do MRU: [a, b] (LRU=b)
    assert client.get('/users/u1/cache/a').status_code == 200

    # POST c -> powinno wyrzucić b (bo b jest LRU)
    assert client.post('/users/u1/cache', json={'doc_id':'c','content':'C'}).status_code in (200,201)

    r = client.get('/users/u1/cache')
    body = r.json()
    assert [i["doc_id"] for i in body["items"]] == ["c","a"]
    assert client.get('/users/u1/cache/b').status_code == 404

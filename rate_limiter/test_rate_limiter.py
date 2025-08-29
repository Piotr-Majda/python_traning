# test_rate_limit_api.py
import pytest
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient

# Zaimportuj swoje:
# from token_bucket import TokenBucket, Clock  # jeśli potrzebne
from .rate_limiter import rate_limiter, Buckets  # -> Twoja fabryka zależności

class FakeClock:
    def __init__(self, t0: float = 0.0):
        self.t = t0
    def now(self) -> float:
        return self.t
    def wait(self, dt: float) -> None:
        self.t += dt
    def advance(self, dt: float) -> None:
        self.t += dt

@pytest.fixture()
def app_and_clock():
    clk = FakeClock()
    app = FastAPI()

    # rate=2 tok/s, capacity=3
    dep = rate_limiter(rate=2.0, capacity=3, clock=clk)

    @app.get("/ping", dependencies=[Depends(dep)])
    def ping():
        return {"ok": True}

    return app, clk

def test_burst_and_recovery(app_and_clock):
    app, clk = app_and_clock
    client = TestClient(app)

    # burst do capacity
    assert client.get("/ping").status_code == 200
    assert client.get("/ping").status_code == 200
    assert client.get("/ping").status_code == 200

    # brak tokena
    r = client.get("/ping")
    assert r.status_code == 429
    assert r.json()["detail"] == "rate limit exceeded"

    # po 0.5 s przy 2 tok/s -> ~1 token
    clk.advance(0.5)
    assert client.get("/ping").status_code == 200

    # znów pustka
    assert client.get("/ping").status_code == 429

    # kolejna połówka sekundy -> znów 1 token
    clk.advance(0.5)
    assert client.get("/ping").status_code == 200

def test_separate_ips_have_separate_buckets():
    clk = FakeClock()
    app = FastAPI()
    dep = rate_limiter(rate=1.0, capacity=1, clock=clk)

    @app.get("/res", dependencies=[Depends(dep)])
    def res():
        return {"ok": True}

    client = TestClient(app)

    # IP A
    r1 = client.get("/res", headers={"X-Forwarded-For": "1.1.1.1"})
    assert r1.status_code == 200

    # IP A drugi raz -> 429
    r2 = client.get("/res", headers={"X-Forwarded-For": "1.1.1.1"})
    assert r2.status_code == 429

    # IP B ma osobny kubełek
    r3 = client.get("/res", headers={"X-Forwarded-For": "2.2.2.2"})
    assert r3.status_code == 200


def test_buckets_gc_and_touch():
    class FakeClock:
        def __init__(self): self.t=0.0
        def now(self): return self.t
        def wait(self, dt): self.t += dt

    clk = FakeClock()
    b = Buckets(rate=1.0, capacity=2, clock=clk)

    tb1 = b.get_or_create("ip1")
    clk.wait(60*2 + 0.1)  # > lifespan
    tb2 = b.get_or_create("ip2")
    assert set(b._buckets.keys()) == {"ip1", "ip2"}
    clk.wait(60*3 + 0.1)  # > lifespan
    
    # dotknięcie ip1 odświeża ts, ip2 usunie GC
    tb2_again = b.get_or_create("ip2")
    assert tb2_again is tb2
    assert "ip1" not in b._buckets
    assert "ip2" in b._buckets

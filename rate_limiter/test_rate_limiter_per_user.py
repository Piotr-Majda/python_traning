# test_rate_limit_per_user.py
import pytest
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient

from rate_limiter.rate_limiter import rate_limiter  # <--- Twoja fabryka dependency

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
def app_and_clock_user():
    clk = FakeClock()
    app = FastAPI()

    # per-user: klucz z nagłówka X-User-Id
    dep = rate_limiter(rate=1.0, capacity=1, clock=clk)

    @app.get("/res", dependencies=[Depends(dep)])
    def res():
        return {"ok": True}

    return app, clk

def test_per_user_buckets_are_isolated(app_and_clock_user):
    app, clk = app_and_clock_user
    client = TestClient(app)

    # Ten sam IP, różni użytkownicy -> osobne kubełki
    h_alice = {"X-User-Id": "alice"}
    h_bob = {"X-User-Id": "bob"}

    # alice pierwszy raz -> 200
    r1 = client.get("/res", headers=h_alice)
    assert r1.status_code == 200
    assert r1.headers.get("X-RateLimit-Remaining") == "0"

    # alice drugi raz (bez czasu) -> 429
    r2 = client.get("/res", headers=h_alice)
    assert r2.status_code == 429
    assert r2.headers.get("X-RateLimit-Remaining") == "0"
    assert float(r2.headers.get("Retry-After")) == pytest.approx(1.0, rel=1e-6)

    # bob (ten sam IP, inny user) -> osobny kubełek -> 200
    r3 = client.get("/res", headers=h_bob)
    assert r3.status_code == 200
    assert r3.headers.get("X-RateLimit-Remaining") == "0"

def test_same_user_across_ips_shares_bucket(app_and_clock_user):
    app, clk = app_and_clock_user
    client = TestClient(app)

    # Symulacja „różnych IP” przez X-Forwarded-For,
    # ale per-user klucz wynika z X-User-Id, więc kubełek wspólny.
    headers_ip1 = {"X-User-Id": "carol", "X-Forwarded-For": "1.1.1.1"}
    headers_ip2 = {"X-User-Id": "carol", "X-Forwarded-For": "2.2.2.2"}

    # Pierwsze żądanie usera -> 200
    r1 = client.get("/res", headers=headers_ip1)
    assert r1.status_code == 200
    assert r1.headers.get("X-RateLimit-Remaining") == "0"

    # Drugie żądanie tego samego usera z innego IP -> 429 (ten sam kubełek per-user)
    r2 = client.get("/res", headers=headers_ip2)
    assert r2.status_code == 429
    assert r2.headers.get("X-RateLimit-Remaining") == "0"

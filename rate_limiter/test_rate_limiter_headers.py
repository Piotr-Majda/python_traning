# test_rate_limit_headers.py
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
def app_and_clock():
    clk = FakeClock()
    app = FastAPI()

    # rate=2 tok/s, capacity=3; kluczowanie po IP (domyślnie)
    dep = rate_limiter(rate=2.0, capacity=3, clock=clk)

    @app.get("/ping", dependencies=[Depends(dep)])
    def ping():
        return {"ok": True}

    return app, clk

def test_headers_remaining_and_retry_after(app_and_clock):
    app, clk = app_and_clock
    client = TestClient(app)

    # 1: 200, remaining=2
    r1 = client.get("/ping")
    assert r1.status_code == 200
    assert r1.headers.get("X-RateLimit-Remaining") == "2"

    # 2: 200, remaining=1
    r2 = client.get("/ping")
    assert r2.status_code == 200
    assert r2.headers.get("X-RateLimit-Remaining") == "1"

    # 3: 200, remaining=0
    r3 = client.get("/ping")
    assert r3.status_code == 200
    assert r3.headers.get("X-RateLimit-Remaining") == "0"

    # 4: 429, remaining=0, Retry-After ~0.5s (przy 2 tok/s potrzeba 0.5s na 1 token)
    r4 = client.get("/ping")
    assert r4.status_code == 429
    assert r4.json()["detail"] == "rate limit exceeded"
    assert r4.headers.get("X-RateLimit-Remaining") == "0"
    retry_after = float(r4.headers.get("Retry-After"))
    assert pytest.approx(retry_after, rel=1e-3) == 0.5

    # Po 0.5s -> 1 token, po zużyciu remaining wraca do 0
    clk.advance(0.5)
    r5 = client.get("/ping")
    assert r5.status_code == 200
    assert r5.headers.get("X-RateLimit-Remaining") == "0"

import pytest
from .token_bucket import TokenBucket


class FakeClock:
    def __init__(self, t0: float = 0.0):
        self.t = t0
    def now(self) -> float:
        return self.t
    def advance(self, dt: float) -> None:
        self.t += dt
    def wait(self, time):
        self.t += time

def test_basic_flow():
    clk = FakeClock()
    tb = TokenBucket(rate=2.0, capacity=5, clock=clk)
    # start: pełne 5
    assert tb.allow(3) is True
    assert tb.tokens == pytest.approx(2.0)  # 2 zostały
    assert tb.allow(3) is False             # brak
    clk.advance(2.0)                        # doleci 3.0 tokeny
    assert tb.allow(3) is True              # teraz się uda

def test_never_exceed_capacity():
    clk = FakeClock()
    tb = TokenBucket(rate=10.0, capacity=5, clock=clk)
    clk.advance(100.0)  # minęło mnóstwo czasu
    assert tb.tokens == pytest.approx(5.0)  # nigdy > capacity

def test_n_greater_than_capacity():
    clk = FakeClock()
    tb = TokenBucket(rate=1.0, capacity=5, clock=clk)
    assert tb.allow(6) is False

def test_fractional_rate():
    clk = FakeClock()
    tb = TokenBucket(rate=0.5, capacity=2, clock=clk)  # 0.5 tok/s
    assert tb.allow(2) is True   # start pełny
    assert tb.allow(1) is False  # brak
    clk.advance(1.9)             # ~0.95 tokena napłynęło, ale zaokrągleń nie robimy
    assert tb.allow(1) is False  # jeszcze ciut za mało
    clk.advance(0.2)             # teraz 1.05
    assert tb.allow(1) is True

def test_invalid_args():
    clk = FakeClock()
    with pytest.raises(ValueError):
        TokenBucket(rate=-1.0, capacity=5, clock=clk)
    with pytest.raises(ValueError):
        TokenBucket(rate=1.0, capacity=0, clock=clk)
    tb = TokenBucket(rate=1.0, capacity=5, clock=clk)
    with pytest.raises(ValueError):
        tb.allow(0)
    

# ---------- time_to_available ----------
import math


def test_time_to_available_already_enough():
    clk = FakeClock()
    tb = TokenBucket(rate=2.0, capacity=5, clock=clk)  # start: 5
    assert tb.time_to_available(3) == pytest.approx(0.0)

def test_time_to_available_needs_wait():
    clk = FakeClock()
    tb = TokenBucket(rate=2.0, capacity=5, clock=clk)
    assert tb.allow(5) is True        # wyzeruj wiadro
    # potrzeba 3 tokenów; 2 tok/s => 1.5 s
    wait = tb.time_to_available(3)
    assert wait == pytest.approx(1.5, rel=1e-6)

def test_time_to_available_over_capacity_is_inf():
    clk = FakeClock()
    tb = TokenBucket(rate=10.0, capacity=5, clock=clk)
    assert math.isinf(tb.time_to_available(6))

def test_time_to_available_zero_rate_infinite_when_empty():
    clk = FakeClock()
    tb = TokenBucket(rate=0.0, capacity=2, clock=clk)
    assert tb.allow(2) is True   # 0 tokenów
    assert math.isinf(tb.time_to_available(1))

def test_time_to_available_validates_n():
    clk = FakeClock()
    tb = TokenBucket(rate=1.0, capacity=5, clock=clk)
    with pytest.raises(ValueError):
        tb.time_to_available(0)
    with pytest.raises(ValueError):
        tb.time_to_available(-1)



# ---------- try_acquire_until ----------

def test_try_acquire_until_enough_now():
    clk = FakeClock()
    tb = TokenBucket(rate=1.0, capacity=5, clock=clk)
    assert tb.try_acquire_until(3, clk.now() + 0.0) is True
    # od razu pobrało; zegar bez zmian
    assert tb.tokens == pytest.approx(2.0)
    assert clk.now() == pytest.approx(0.0)


def test_try_acquire_until_succeeds_after_wait_and_advances_time():
    clk = FakeClock()
    tb = TokenBucket(rate=2.0, capacity=5, clock=clk)
    assert tb.allow(5) is True              # 0 tokenów
    needed = tb.time_to_available(3)        # 1.5 s
    deadline = clk.now() + needed + 0.01    # minimalny margines
    assert tb.try_acquire_until(3, deadline) is True
    # powinno „dolecieć”, czas może zostać przesunięty do momentu dostępności
    assert tb.tokens == pytest.approx(0.0)  # 3 z 3 pobrane
    assert clk.now() == pytest.approx(1.5)  # zegar nie cofnął się


def test_try_acquire_until_fails_if_deadline_too_soon_no_state_change():
    clk = FakeClock()
    tb = TokenBucket(rate=1.0, capacity=3, clock=clk)
    assert tb.allow(3) is True              # 0 tokenów
    # potrzeba 2s, dajemy za mały margines
    assert tb.try_acquire_until(2, clk.now() + 1.0) is False
    # brak zmian stanu i czasu
    assert tb.tokens == pytest.approx(0.0)
    assert clk.now() == pytest.approx(0.0)


def test_try_acquire_until_n_greater_than_capacity_is_false():
    clk = FakeClock()
    tb = TokenBucket(rate=100.0, capacity=5, clock=clk)
    assert tb.try_acquire_until(6, clk.now() + 1000.0) is False


def test_try_acquire_until_with_zero_rate_only_if_already_enough():
    clk = FakeClock()
    tb = TokenBucket(rate=0.0, capacity=3, clock=clk)
    assert tb.try_acquire_until(2, clk.now() + 10.0) is True   # start pełny
    assert tb.try_acquire_until(2, clk.now() + 10.0) is False  # nie doleci nigdy


def test_try_acquire_until_invalid_args():
    clk = FakeClock()
    tb = TokenBucket(rate=1.0, capacity=5, clock=clk)
    with pytest.raises(ValueError):
        tb.try_acquire_until(0, clk.now() + 1.0)
    with pytest.raises(ValueError):
        tb.try_acquire_until(-1, clk.now() + 1.0)

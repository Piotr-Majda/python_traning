from __future__ import annotations
from typing import Protocol

class Clock(Protocol):
    def wait(self, dt: float) -> None: ...
    def now(self) -> float: ...

class TokenBucket:
    """
    Continuous token bucket:
      - rate: tokens per second (float, >= 0)
      - capacity: max tokens (int > 0)
    Starts full (capacity).
    """
    def __init__(self, rate: float, capacity: int, clock: Clock) -> None:
        if capacity <= 0:
            raise ValueError("Capacity must be a positive integer")
        if rate < 0:
            raise ValueError("Rate must be non-negative")
        self._rate: float = float(rate)
        self._capacity: int = int(capacity)
        self._clock: Clock = clock
        self._tokens: float = float(capacity)
        self._last_refill: float = self._clock.now()

    def _refill_bucket(self) -> None:
        now = self._clock.now()
        elapsed = now - self._last_refill
        if elapsed > 0 and self._rate > 0.0:
            self._tokens = min(self._capacity, self._tokens + elapsed * self._rate)
        self._last_refill = now

    def allow(self, tokens: int = 1) -> bool:
        if tokens <= 0:
            raise ValueError("Requested tokens must be positive")
        if tokens > self._capacity:
            return False
        self._refill_bucket()
        if self._tokens >= tokens:
            self._tokens -= tokens
            return True
        return False

    @property
    def tokens(self) -> float:
        self._refill_bucket()
        return self._tokens

    def time_to_available(self, tokens: int) -> float:
        self._refill_bucket()
        if tokens <= 0:
            raise ValueError("Requested tokens must be positive")
        if tokens <= self._tokens:
            return 0.0
        if tokens > self._capacity:
            return float('inf')
        if self._rate == 0.0:
            return float('inf')
        missing = tokens - self._tokens
        return missing / self._rate

    def try_acquire_until(self, tokens: int, deadline: float) -> bool:
        if tokens <= 0:
            raise ValueError("Tokens must be positive")
        if tokens > self._capacity:
            return False

        self._refill_bucket()
        now = self._clock.now()

        # mamy już dość?
        if self._tokens >= tokens:
            self._tokens -= tokens
            return True

        # ile trzeba czekać i ile czasu zostało?
        wait = self.time_to_available(tokens)  # już po refillu, więc bazuje na aktualnym stanie
        time_left = deadline - now
        if wait > time_left or time_left < 0:
            return False

        # "czekamy" i pobieramy
        self._clock.wait(wait)
        self._refill_bucket()
        if self._tokens >= tokens:
            self._tokens -= tokens
            return True
        # Teoretycznie nie powinno się zdarzyć (zaokrąglenia itp.), ale bądźmy ostrożni:
        return False

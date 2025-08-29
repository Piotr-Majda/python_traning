"""
Zadanie #8 — Rate limit w FastAPI z TokenBucket (per-IP)

Cel:
Użyj swojej klasy TokenBucket do ograniczania liczby żądań na endpoint w FastAPI.

Interfejs:
- Fabryka zależności: rate_limit(rate: float, capacity: int, clock: Clock | None = None) -> Depends
- Zegar: użyj Twojego interfejsu Clock (RealClock/FakeClock). RealClock oparte o time.monotonic.

Wymagania funkcjonalne:
1) Limit liczony per-IP (klucz: request.client.host).
2) Każde wywołanie endpointu „kosztuje” 1 token (allow(1)).
3) Jeśli brak tokenów → HTTP 429 + JSON: {"detail": "rate limit exceeded"}.
4) Pojemność (capacity) i napływ (rate, tokeny/sek) muszą działać jak w Twoim ciągłym buckecie.
5) Pamięć in-memory: dict[ip] -> (TokenBucket, last_seen_ts).
6) Opcjonalnie: prosty GC — usuń kubełek nieużywany > 5 min (wywoływany „przy okazji” każdego requestu).

Wymagania techniczne:
- Zero blokujących sleepów w dependency (RealClock może mieć sleep, ale w testach użyj FakeClock).
- Dependency nie może modyfikować globalnego stanu poza swoją mapą kubełków.
- Brak zewnętrznych serwisów (Redis itp.) w tej wersji.

Akceptacja:
- Testy poniżej przechodzą.
- Ręcznie: przy rate=2.0, capacity=3 — trzy pierwsze /ping zwracają 200, czwarty 429; po „upływie” 0.5s wraca 200.

Dostarcz:
- `rate_limit.py` (dependency, RealClock).
- `app.py` (FastAPI z endpointem /ping i podpiętym limiterem).
- Twoje istniejące `token_bucket.py` (z Clock/TokenBucket).
"""
from typing import Optional
from fastapi import Header, HTTPException, Request, Response
from pydantic import BaseModel
from token_bucket.token_bucket import TokenBucket, Clock


class Buckets:
    def __init__(self, rate: float, capacity: int, clock: Clock):
        self._clock = clock
        self._tb_factory = lambda: TokenBucket(rate, capacity, clock)
        self._buckets: dict[str, tuple[TokenBucket, float]] = {}  # name -> (bucket, last_seen)
        self._lifespan = 60 * 5  # 5 min

    def _gc(self) -> None:
        now = self._clock.now()
        stale = [name for name, (_, ts) in self._buckets.items() if (now - ts) > self._lifespan]
        for name in stale:
            self._buckets.pop(name, None)

    def get_or_create(self, name: str) -> TokenBucket:
        self._gc()
        now = self._clock.now()
        if name in self._buckets:
            bucket, _ = self._buckets[name]
            self._buckets[name] = (bucket, now)
            return bucket
        bucket = self._tb_factory()
        self._buckets[name] = (bucket, now)
        return bucket

class CommonHeaders(BaseModel):
    x_forwarded_for: str
    x_user_id: str

def _extract_client_key(request: Request, headers: CommonHeaders) -> str:
    if headers.x_user_id:
        return headers.x_user_id.strip()
    if headers.x_forwarded_for:
        return headers.x_forwarded_for.split(",")[0].strip()
    return request.client.host if request.client else "unknown"

def rate_limiter(rate: float, capacity: int, clock: Clock):
    buckets = Buckets(rate, capacity, clock)

    async def verify_limit(
        request: Request,
        response: Response,
        x_forwarded_for: Optional[str] = Header(None, alias="X-Forwarded-For"),
        x_user_id: Optional[str] = Header(None, alias="X-User-Id"),
    ):
        # Stwórz obiekt CommonHeaders ręcznie
        common_headers = CommonHeaders(
            x_forwarded_for=x_forwarded_for or "",
            x_user_id=x_user_id or "",
        )
        key = _extract_client_key(request, common_headers)
        tb = buckets.get_or_create(key)
        
        is_allow = tb.allow(1)
        remaining_tokens = int(tb.tokens)
        headers = {'X-RateLimit-Remaining': str(remaining_tokens)}
        if not is_allow:
            retry_time = tb.time_to_available(1)
            headers['Retry-After'] = str(retry_time)
            raise HTTPException(
                status_code=429,
                detail="rate limit exceeded", 
                headers=headers
                )
        response.headers.update(headers)

    return verify_limit

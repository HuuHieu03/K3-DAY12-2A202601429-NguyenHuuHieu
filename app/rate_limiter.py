"""CP3 — Rate limiting bằng thuật toán sliding window.

Đếm số request trong 60 giây **gần nhất** (cửa sổ trượt), thay vì đếm theo
phút đồng hồ. Đếm theo phút đồng hồ có lỗ hổng: 10 request lúc 10:00:59 và
10 request lúc 10:01:01 = 20 request trong 2 giây mà vẫn "đúng luật".

Cấu trúc dữ liệu: Redis Sorted Set (ZSET), score = timestamp của request.
"""

from __future__ import annotations

import time
import uuid

from fastapi import HTTPException, status

WINDOW_SECONDS = 60


class RateLimiter:
    def __init__(self, client, limit_per_minute: int) -> None:
        self.client = client
        self.limit = limit_per_minute

    def _key(self, user_id: str) -> str:
        """Redis key for a user's rate‑limit sorted set."""
        return f"ratelimit:{user_id}"

    def hit_count(self, user_id: str, now: float | None = None) -> int:
        """Return the number of requests made by *user_id* in the last WINDOW_SECONDS.

        This method only cleans up old entries and returns the current count.
        It does **not** record a new request.
        """
        now = now if now is not None else time.time()
        key = self._key(user_id)
        # Remove entries older than the sliding window
        self.client.zremrangebyscore(key, 0, now - WINDOW_SECONDS)
        # Return current count
        return self.client.zcard(key)

    def check(self, user_id: str, now: float | None = None) -> None:
        """Enforce the rate limit.

        Raises ``HTTPException`` with status 429 if the request would exceed the
        configured limit. Otherwise records the request in Redis.
        """
        now = now if now is not None else time.time()
        key = self._key(user_id)
        # Refresh window and get current count
        count = self.hit_count(user_id, now)
        if count >= self.limit:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="rate limit exceeded",
                headers={"Retry-After": str(WINDOW_SECONDS)},
            )
        # Record this request with a unique member to avoid collisions
        member = f"{now}:{uuid.uuid4().hex}"
        self.client.zadd(key, {member: now})
        self.client.expire(key, WINDOW_SECONDS)

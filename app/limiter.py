import time
import redis.asyncio as aioredis
from app.config import settings

redis_client = aioredis.from_url(settings.REDIS_URL, decode_responses=True)

async def is_allowed(client_key: str) -> tuple[bool, int, int]:
    """
    Sliding window rate limiter using Redis.
    Returns: (allowed, current_count, remaining)
    """
    window_key = f"ratelimit:{client_key}:{int(time.time() // settings.WINDOW_SECONDS)}"

    pipe = redis_client.pipeline()
    pipe.incr(window_key)
    pipe.expire(window_key, settings.WINDOW_SECONDS)
    results = await pipe.execute()

    current = results[0]
    remaining = max(0, settings.MAX_REQUESTS - current)
    allowed = current <= settings.MAX_REQUESTS

    return allowed, current, remaining
"""Lightweight Redis-backed JSON cache decorator for async endpoints.

Usage:
    @cache(ttl=300, prefix="page")
    async def get_page(slug: str, lang: Lang = Depends(get_lang), ...): ...

The decorator hashes selected kwargs (str/int/bool only) into a key.
DB sessions and other complex objects are ignored automatically.
"""
import functools
import hashlib
import json
import logging
from typing import Any, Callable

from app.redis_client import redis_client

log = logging.getLogger("xiuedu.cache")

_PRIMITIVE = (str, int, float, bool, type(None))


def _build_key(prefix: str, kwargs: dict[str, Any]) -> str:
    parts = []
    for k in sorted(kwargs):
        v = kwargs[k]
        if isinstance(v, _PRIMITIVE):
            parts.append(f"{k}={v}")
    raw = "|".join(parts)
    digest = hashlib.md5(raw.encode("utf-8")).hexdigest()[:16]
    return f"cache:{prefix}:{digest}"


def cache(ttl: int, prefix: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            key = _build_key(prefix, kwargs)
            try:
                hit = await redis_client.get(key)
                if hit:
                    return json.loads(hit)
            except Exception as e:  # noqa: BLE001
                log.warning("cache get failed: %s", e)

            result = await func(*args, **kwargs)

            try:
                payload = json.dumps(result, default=str)
                await redis_client.setex(key, ttl, payload)
            except Exception as e:  # noqa: BLE001
                log.warning("cache set failed: %s", e)
            return result

        return wrapper

    return decorator


async def invalidate(prefix: str) -> None:
    """Delete all cached entries for a given prefix."""
    pattern = f"cache:{prefix}:*"
    try:
        async for key in redis_client.scan_iter(match=pattern, count=200):
            await redis_client.delete(key)
    except Exception as e:  # noqa: BLE001
        log.warning("cache invalidate failed: %s", e)

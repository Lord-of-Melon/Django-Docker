from django.core.cache import cache
from ninja.errors import HttpError


RATE_LIMIT = 60
WINDOW = 60  # detik


def rate_limit(request):

    # Ambil IP client
    ip = request.META.get("REMOTE_ADDR", "unknown")

    cache_key = f"rate_limit:{ip}"

    current = cache.get(cache_key)

    if current is None:
        cache.set(cache_key, 1, timeout=WINDOW)
        return

    if current >= RATE_LIMIT:
        raise HttpError(
            429,
            "Rate limit exceeded. Maksimal 60 request per menit."
        )

    cache.incr(cache_key)
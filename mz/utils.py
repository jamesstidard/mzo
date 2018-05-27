import asyncio

from collections import Awaitable
from functools import wraps


def async_command(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        result = f(*args, **kwargs)
        if isinstance(result, Awaitable):
            loop = asyncio.get_event_loop()
            return loop.run_until_complete(result)
        else:
            return result
    return wrapper

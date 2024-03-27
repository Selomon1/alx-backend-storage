#!/usr/bin/env python3
"""
get page module
"""

import requests
import redis
import time
from functools import wraps


# Initialize Redis Client
redis_client = redis.Redis()


def count_access(func):
    """
    Decorator to track URL access
    """
    @wraps(func)
    def wrapper(url):
        count_key = f"count:{url}"
        redis_client.incr(count_key)
        return func(url)
    return wrapper


def cache_expiry(func):
    """
    Decorator to cache
    """
    @wraps(func)
    def wrapper(url):
        cache_key = f"cache:{url}"
        cached_result = redis_client.get(cache_key)
        if cached_result:
            return cached_result.decode('utf-8')
        else:
            result = dunc(url)
            redis_client.setex(cache_key, 10, result)
            return result
        return wrapper


@count_access
@cache_expiry
def get_page(url: str) -> str:
    """
    Fetch the HTML content of a given URL
    """
    response = requests.get(url)
    return response.text

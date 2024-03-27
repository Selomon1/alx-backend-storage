#!/usr/bin/env python3
"""
get page module
"""

import requests
import redis
from typing import Callable
from functools import wraps


def count_access(func: Callable) -> Callable:
    """
    Decorator to track URL access
    Param:
        call: the call function which is Callable

    Returns:
        wrapper that tracks the count of access to url
    """
    @wraps(func)
    def wrapper(url: str) -> str:
        """
        Retrieves the HTML content of the given URL
        Params:
            url: the URL
        Returns:
            the HTML retrieved from the URL
        """
        redis_client = redis.Redis()
        redis_client.incr(f"count:{url}")

        cached_content = redis_client.get(url)
        if cached_content:
            return cached_content.decode('utf-8')
        else:
            response = func(url)
            redis_client.set(url, 10, response)
            return response
    return wrapper


@count_access
def get_page(url: str) -> str:
    """
    Fetch the HTML content of a given URL
    Params:
        url: the given URL
    Returns:
        the HTML retrieved from the URL
    """
    response = requests.get(url)
    return response.text

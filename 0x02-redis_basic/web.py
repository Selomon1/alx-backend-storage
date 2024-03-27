#!/usr/bin/env python3
"""
get page module
"""

import requests
import redis
from typing import Callable
from functools import wraps


def count_access(calls: Callable) -> Callable:
    """
    Decorator to track URL access
    Param:
        call: the call function which is Callable

    Returns:
        wrapper that tracks the count of access to url
    """
    @wraps(calls)
    def wrapper(url):
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
            response = requests.get(url)
            page_content = response.text
            redis_client.setex(url, 10, page_content)
        return page_content
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

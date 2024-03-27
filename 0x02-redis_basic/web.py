#!/usr/bin/env python3
"""
get page module
"""

import requests
import redis
import time


# Initialize Redis client
redis_client = redis.Redis()


def get_page(url: str) -> str:
    """
    Fetch the HTML content of a given URL
    """
    # Increment the count for the URL
    count_key = f"count:{url}"
    redis_client.incr(count_key)

    # Get the HTML content
    response = requests.get(url)
    html_content = response.text

    # cache the HTML
    cache_key = f"cache:{url}"
    redis_client.setex(cache_key, 10, html_content)

    return html_content

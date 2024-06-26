#!/usr/bin/env python3
"""
Redis basic tasks
"""
import redis
from typing import Callable, Optional, Union
from functools import wraps
import uuid


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of times a method is called
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper func to increment call count and call the original method
        """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs for part. function.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function to store input and output history, and call the orgi
        """
        key = method.__qualname__
        inputs_key = f"{key}:inputs"
        outputs_key = f"{key}:outputs"
        self._redis.rpush(inputs_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(outputs_key, output)
        return output
    return wrapper


class Cache:
    """
    Cache class interact with Redis
    """

    def __init__(self) -> None:
        """
        Initialize the Cache instances and flash the redis data
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        generates random key, store the input data in Redis
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None):
        """
        Retrieves data from Redis using the key and optionally applies
        a conversion function
        """
        value = self._redis.get(key)
        if value is not None and fn is not None:
            return fn(value)
        return value

    def get_str(self, key: str) -> Union[str, None]:
        """
        Retrieves data from Redis using the key & convert it to a string
        """
        value = self._redis.get(key)
        if value is not None:
            return value.decode('utf-8')
        return None

    def get_int(self, key: str) -> Union[int, None]:
        """
        Retrieves data from Redis using the key & converts it to an integer
        """
        value = self._redis.get(key)
        if value is not None:
            return int(value.decode("utf-8"))
        return None


def replay(method: Callable) -> None:
    """
    Function to display the history of calls of particular function
    """
    key = method.__qualname__
    inputs_key = f"{key}:inputs"
    outputs_key = f"{key}:outputs"
    redis = method.__self__._redis
    totalCalls = int(redis.get(key).decode("utf-8"))
    print(f"{key} was called {totalCalls} times:")
    inputs = redis.lrange(inputs_key, 0, -1)
    outputs = redis.lrange(outputs_key, 0, -1)
    for i, j in zip(inputs, outputs):
        print(f"{key}(*{i.decode('utf-8')}) -> {j.decode('utf')}")

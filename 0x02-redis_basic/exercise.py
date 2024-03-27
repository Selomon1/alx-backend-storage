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

    def get(self, key: str, fn: Optional[Callable] = None)
        -> Union[str, bytes, int, float]:
        """
        Retrieves data from Redis using the key and optionally applies
        a conversion function
        """
        value = self._redis.get(key)
        if value is not None and fn is not None:
            return fn(value)
        return value

    def get_str(self, key: str) -> str:
        """
        Retrieves data from Redis using the key & convert it to a string
        """
        return self.get(key, fn=lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """
        Retrieves data from Redis using the key & converts it to an integer
        """
        return self.get(key, fn=int)

def replay(method: Callable) -> None:
    """
    Function to display the history of calls of particular function
    """
    key = method.__qualname__
    inputs_key = f"{key}:inputs"
    outputs_key = f"{key}:outputs"
    inputs = self._redis.lrange(inputs_key, 0, -1)
    outputs = self._redis.lrange(outputs_key, 0, -1)
    print(f"{key} was called {len(inputs)} times:")
    for input_, output in zip(inputs, outputs):
        print(f"{key}(*{input_}) -> {output}")

#!/usr/bin/env python3
"""
Redis basic tasks
"""
import redis
from typing import Callable
import functools
import uuid


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

    def store(self, data) -> str:
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
        if value is not None:
            if fn is not None:
                return fn(value)
            return value
        return None

    def get_str(self, key: str):
        """
        Retrieves data from Redis using the key & convert it to a string
        """
        return self.get(key, fn=lambda x: x.decode())

    def get_int(self, key: str):
        """
        Retrieves data from Redis using the key & converts it to an integer
        """
        return self.get(key, fn=int)

    def count_calls(method):
        """
        Decorator to count
        """
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            key = method.__qualname__
            self._redis.incr(key)
            return method(self, *args, **kwargs)
        return wrapper

    @count_calls
    def store(self, data) -> str:
        """
        Generates a random key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def call_history(method):
        """
        decorator to store the history
        """
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            key = method.__qualname__
            inputs_key = f"{key}:inputs"
            outputs_key = f"{key}:outputs"
            self._redis.rpush(inputs_key, str(args))
            output = method(self, *args, **kwargs)
            self._redis.rpush(outputs_key, output)
            return output
        return wrapper

    @call_history
    def store(self, data) -> str:
        """
        Generates random key, store the input data in Redis
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def replay(method):
        """
        Function to display the history of calls o
        """
        key = method.__qualname__
        inputs_key = f"{key}:inputs"
        outputs_key = f"{key}:outputs"
        inputs = self._redis.lrange(inputs_key, 0, -1)
        outputs = self._redis.lrange(outputs_key, 0, -1)
        print(f"{key} was called {len(inputs)} times:")
        for input_, output in zip(inputs, outputs):
            print(f"{key}(*{input_}) -> {output}")

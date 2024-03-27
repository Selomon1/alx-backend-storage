# 0x02-redis_basic
This project contains Python code for interacting with Redis, implementing various tasks related to storing, retrieving, and managing data using Redis.

## Tasks

### 0. Writing strings to Redis

Create a Cache class that interacts with Redis. Implement a `store` method to store data in Redis using a random key.

### 1. Reading from Redis and recovering original type

Implement a `get` method in the Cache class to retrieve data from Redis and optionally convert it back to the original type.

### 2. Incrementing values

Implement a decorator `count_calls` to count the number of times a method is called and decorate the `store` method with it.

### 3. Storing lists

Implement a decorator `call_history` to store the history of inputs and outputs for a function and decorate the `store` method with it.

### 4. Retrieving lists

Implement a function `replay` to display the history of calls of a particular function.

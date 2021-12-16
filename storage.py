import functools
import json
import random
import tarantool
import time


MIN_TIMEOUT = 0.1
MAX_TIMEOUT = 15 * 60
TIMEOUT_FACTOR = 2
TIMEOUT_JITTER = 0.1
ATTEMPTS = 20


def retrys(attempts):
    def decorator(f, *args, **kwargs):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            delay = MIN_TIMEOUT
            for i in range(attempts):
                try:
                    return f(*args, **kwargs)
                except (TimeoutError, ConnectionError) as e:
                    time.sleep(delay)
                    delay = min(delay * TIMEOUT_FACTOR, MAX_TIMEOUT)
                    delay = max(random.gauss(delay, TIMEOUT_JITTER), MIN_TIMEOUT)
            raise ConnectionError("Connection failed after {} attempts".format(attempts))

        return wrapper

    return decorator


class TarantoolConnection:
    def __init__(
        self,
        host="localhost",
        port=3301,
        user="username",
        password="password",
        timeout=3,
    ):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.user = user
        self.password = password
        self.connection = self.get_connection()

    def get_connection(self):
        connection = tarantool.connect(self.host, self.port, self.user, self.password)
        return connection.space(0)

    @retrys(ATTEMPTS)
    def get(self, key):
        try:
            value = self.connection.select(key)
            if value is not None:
                return value
        except tarantool.error.NetworkError as e:
            raise ValueError(e)
        except Exception as e:
            raise ValueError(e)

    @retrys(ATTEMPTS)
    def cache_get(self, key):
        return self.get(key)

    @retrys(ATTEMPTS)
    def set(self, key, value):
        try:
            self.connection.insert(key, value)
            return True
        except tarantool.error.NetworkError as e:
            raise ValueError(e)
        except Exception as e:
            raise ValueError(e)

    @retrys(ATTEMPTS)
    def cache_set(self, key, value):
        return self.set(key, value)

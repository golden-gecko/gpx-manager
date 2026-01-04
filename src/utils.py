import functools
import time

from logger import Logger


def get_time() -> float:
    return time.time()


def get_duration(start_time) -> float:
    return time.time() - start_time


def print_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = get_time()
        result = func(*args, **kwargs)

        logger = Logger(__name__)
        logger.debug(f'Function {func.__name__} finished in {get_duration(start_time):.2f} seconds')

        return result

    return wrapper

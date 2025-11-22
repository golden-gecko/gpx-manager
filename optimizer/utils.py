import functools
import time


def get_time():
    return time.time()


def get_duration(start_time):
    return time.time() - start_time


def print_time(func):
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        start_time = get_time()
        result = func(*args, **kwargs)
        print(F'Function {func.__name__} finished in {get_duration(start_time):.2f} seconds')
        return result

    return new_func

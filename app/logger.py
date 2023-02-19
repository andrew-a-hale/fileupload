import logging
import typing
from functools import wraps


def setup_logger(logging_level: int) -> None:
    logging.basicConfig(level=logging_level,
                        format="%(levelname)s: %(asctime)s %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")


def log_decorator(func: typing.Callable) -> typing.Callable:

    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f'{func.__module__}.{func.__name__} called')
        func(*args, **kwargs)

    return wrapper


def log_debug_decorator(func: typing.Callable) -> typing.Callable:

    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.debug(
            f'{func.__module__}.{func.__name__} called with args: {str(args)} and kwargs: {str(kwargs)}'
        )
        func(*args, **kwargs)

    return wrapper
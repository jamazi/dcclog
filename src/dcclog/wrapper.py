import inspect
import logging
from functools import wraps
from time import perf_counter_ns
from typing import Any, Callable, Optional, TypeVar, Union, overload

from dcclog.logger import getLogger

R = TypeVar("R")
F = TypeVar("F", bound=Callable[..., Any])


@overload
def log(func: F) -> F:
    ...


@overload
def log(
    *,
    logger: Optional[logging.Logger] = None,
    level: int = logging.DEBUG,
    stacklevel: int = 2,
    nested: bool = False,
    minimal_latency_ms: int = 100,
    skip_args: int = 0,
) -> Callable[[F], F]:
    ...


def log(
    func: Optional[Callable[..., R]] = None,
    *,
    logger: Optional[logging.Logger] = None,
    level: int = logging.DEBUG,
    stacklevel: int = 2,
    nested: bool = False,
    minimal_latency_ms: int = 100,
    skip_args: int = 0,
) -> Union[Callable[[Callable[..., R]], Callable[..., R]], Callable[..., R]]:
    def get_caller_info(func: Callable[..., R]) -> dict[str, Any]:
        try:
            real_func = inspect.unwrap(func)
            if real_func is None:
                real_func = func
        except ValueError:
            real_func = func
        if real_func:
            return {
                "filename": real_func.__code__.co_filename,
                "lineno": real_func.__code__.co_firstlineno,
            }
        return {}

    def format_latency(t: int) -> str:
        if t >= minimal_latency_ms * 1e6:
            if t >= 1e9:
                return f" Execution time: {round(t / 1e9, 3)}s"
            return f" Execution time: {round(t / 1e6, 3)}ms"
        return ""

    def decorator(func: Callable[..., R]) -> Callable[..., R]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> R:
            nonlocal logger

            logger = logger or getLogger(func.__module__)

            args_repr = list(map(repr, args[skip_args:]))
            kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
            signature = ", ".join(args_repr + kwargs_repr)

            caller_info = (
                {"caller_info": get_caller_info(func)} if nested else {}
            )

            try:
                timer = perf_counter_ns()
                result = func(*args, **kwargs)
                timer = perf_counter_ns() - timer
            except Exception as exp:
                timer = perf_counter_ns() - timer
                logger.log(
                    level,
                    "Function %s called with args: (%s), raised exception.%s",
                    func.__qualname__,
                    signature,
                    format_latency(timer),
                    exc_info=exp,
                    stacklevel=stacklevel,
                    extra=caller_info,
                )
                raise exp
            logger.log(
                level,
                "Function %s called with args: (%s), returned: %r.%s",
                func.__qualname__,
                signature,
                result,
                format_latency(timer),
                stacklevel=stacklevel,
                extra=caller_info,
            )
            return result

        return wrapper

    if func is not None:
        if callable(func):
            return decorator(func)
        raise TypeError(f"{func!r} is not a callable.")

    return decorator

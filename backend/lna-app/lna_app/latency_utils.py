# pyre-ignore-all-errors
# pyright: reportUndefinedVariable=false, reportGeneralTypeIssues=false

import inspect
import logging
import time
from collections.abc import Awaitable
from contextlib import ContextDecorator
from functools import wraps
from time import perf_counter
from typing import Callable, Optional, ParamSpec, TypeVar, overload

P = ParamSpec("P")
R = TypeVar("R")


@overload
def timeit(func: Callable[P, R]) -> Callable[P, R]: ...
@overload
def timeit(func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]: ...


def timeit(func) -> None:
    """
    Decorator to print how long a function or async function takes (in ms).
    """
    if inspect.iscoroutinefunction(func):

        @wraps(func)
        async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            start = perf_counter()
            result = await func(*args, **kwargs)
            elapsed_ms = (perf_counter() - start) * 1_000
            print(f"{func.__qualname__!r} took {elapsed_ms:.2f} ms")
            return result

        return async_wrapper  # type: ignore
    else:

        @wraps(func)
        def sync_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            start = perf_counter()
            result = func(*args, **kwargs)
            elapsed_ms = (perf_counter() - start) * 1_000
            print(f"{func.__qualname__!r} took {elapsed_ms:.2f} ms")
            return result

        return sync_wrapper  # type: ignore


class measure_latency(ContextDecorator):
    """
    Context manager (and decorator) that logs elapsed time.
    Works as both:
      • sync:   with measure_latency("task"): ...
      • async:  async with measure_latency("task"): ...
      • sync decorator on defs
    """

    def __init__(self, name: str, logger: Optional[logging.Logger] = None) -> None:
        self.name = name
        self._start: float = 0.0

    # sync entry/exit
    def __enter__(self) -> None:
        self._start = time.perf_counter()

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[type[BaseException]],
    ) -> bool:
        elapsed = (time.perf_counter() - self._start) * 1_000
        print(f"[{self.name}] took {elapsed:.2f} ms")
        return False

    # async entry/exit
    async def __aenter__(self) -> None:
        self._start = time.perf_counter()

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[type[BaseException]],
    ) -> bool:
        elapsed = (time.perf_counter() - self._start) * 1_000
        print(f"[{self.name}] took {elapsed:.2f} ms")
        return False

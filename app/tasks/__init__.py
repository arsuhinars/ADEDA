import asyncio
from traceback import format_exception
from typing import Callable, Coroutine
from functools import wraps

from starlette.concurrency import run_in_threadpool

# Список со всеми повторяемыми функциями
# Позже main.py выполняет их при запуске сервера
repated_tasks: list[Coroutine] = []

NoArgsNoReturnFuncT = Callable[[], None]
NoArgsNoReturnAsyncFuncT = Callable[[], Coroutine[any, any, None]]
NoArgsNoReturnDecorator = Callable[[NoArgsNoReturnFuncT | NoArgsNoReturnAsyncFuncT], NoArgsNoReturnAsyncFuncT]

def repeat_every(
    *,
    seconds: float,
    wait_first: bool = False,
    raise_exceptions: bool = False,
    print_log: bool = True,
    max_repetitions: int | None = None,
) -> NoArgsNoReturnDecorator:
    """
    This function returns a decorator that modifies a function so it is periodically re-executed after its first call.
    The function it decorates should accept no arguments and return nothing. If necessary, this can be accomplished
    by using `functools.partial` or otherwise wrapping the target function prior to decoration.
    Parameters
    ----------
    seconds: float
        The number of seconds to wait between repeated calls
    wait_first: bool (default False)
        If True, the function will wait for a single period before the first call
    logger: Optional[logging.Logger] (default None)
        The logger to use to log any exceptions raised by calls to the decorated function.
        If not provided, exceptions will not be logged by this function (though they may be handled by the event loop).
    raise_exceptions: bool (default False)
        If True, errors raised by the decorated function will be raised to the event loop's exception handler.
        Note that if an error is raised, the repeated execution will stop.
        Otherwise, exceptions are just logged and the execution continues to repeat.
        See https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.loop.set_exception_handler for more info.
    max_repetitions: Optional[int] (default None)
        The maximum number of times to call the repeated function. If `None`, the function is repeated forever.
    """

    def decorator(func: NoArgsNoReturnAsyncFuncT | NoArgsNoReturnFuncT) -> NoArgsNoReturnAsyncFuncT:
        """
        Converts the decorated function into a repeated, periodically-called version of itself.
        """
        is_coroutine = asyncio.iscoroutinefunction(func)

        @wraps(func)
        async def wrapped() -> None:
            repetitions = 0

            async def loop() -> None:
                nonlocal repetitions
                if wait_first:
                    await asyncio.sleep(seconds)
                while max_repetitions is None or repetitions < max_repetitions:
                    try:
                        if is_coroutine:
                            await func()
                        else:
                            await run_in_threadpool(func)
                        repetitions += 1
                    except Exception as exc:
                        if print_log:
                            formatted_exception = \
                                f'{func.__name__} (Repeat function) error: \n'
                            formatted_exception += ''.join(
                                format_exception(
                                    type(exc), exc, exc.__traceback__
                                )
                            )
                        if raise_exceptions:
                            raise exc
                    await asyncio.sleep(seconds)

            asyncio.ensure_future(loop())

        repated_tasks.append(wrapped)

        return wrapped
    
    return decorator

from .parser import *

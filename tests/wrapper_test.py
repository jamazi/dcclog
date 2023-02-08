import time
from random import randint

import pytest

from dcclog import DEBUG, ConsoleHandler, Formatter, getLogger, log

handler = ConsoleHandler(formatter=Formatter("%(message)s"))
logger = getLogger("test", level=DEBUG, handlers=handler)

latency_ms = randint(50, 150)


@log(logger=logger)
def divide(a: int, b: int) -> int:
    return int(a / b)


@log(logger=logger, minimal_latency_ms=latency_ms)
def function_with_sleep(ms: int) -> None:
    time.sleep(ms / 1e3)


def test_log(caplog: pytest.LogCaptureFixture) -> None:
    a = 30
    b = 5

    r = divide(a, b)

    assert r == int(a / b)
    assert f"called with args: ({a}, {b}), returned: {r}." in caplog.text


def test_log_exception(caplog: pytest.LogCaptureFixture) -> None:
    a = 15
    b = 0

    with pytest.raises(ZeroDivisionError):
        divide(a, b)

    assert f"called with args: ({a}, {b}), raised exception." in caplog.text


def test_log_no_latency(caplog: pytest.LogCaptureFixture) -> None:
    function_with_sleep(latency_ms - 30)
    assert "Execution time:" not in caplog.text


def test_log_with_latency(caplog: pytest.LogCaptureFixture) -> None:
    function_with_sleep(latency_ms + 30)
    assert "Execution time:" in caplog.text

from __future__ import annotations

import logging
from copy import copy
from typing import Any, Callable, Literal, Optional, Union

from dcclog.cipher import Cipher
from dcclog.colors import Colors


class Formatter(logging.Formatter):
    _color_fn: Optional[Callable[[int], str]] = None
    _DEFAULT_FORMAT = (
        "%(asctime)s :: %(levelname)-8s :: %(name)s"
        " :: %(message)s :: %(filename)s:%(lineno)d"
    )

    def __init__(
        self,
        fmt: str = _DEFAULT_FORMAT,
        *,
        color: Union[Literal[False, True], Callable[[int], str]] = False,
        cipher: Optional[Cipher] = None,
        escape_newline: Optional[str] = None,
        **kwargs: Any,
    ):
        super().__init__(fmt, **kwargs)
        self.set_color(color)
        self.set_cipher(cipher)
        self._escape_newline = escape_newline

    def set_cipher(self, cipher: Optional[Cipher] = None) -> Formatter:
        self._cipher = cipher
        return self

    def set_color(
        self, color: Union[Literal[False, True], Callable[[int], str]]
    ) -> Formatter:
        if color is True:
            self._color_fn = self.default_color_fn
        elif color is False:
            self._color_fn = None
        elif callable(color):
            self._color_fn = color
        return self

    def format(self, record: logging.LogRecord) -> str:
        caller_info = getattr(record, "caller_info", {})
        if caller_info:
            record = copy(record)
            if "filename" in caller_info:
                setattr(record, "filename", caller_info["filename"])
            if "lineno" in caller_info:
                setattr(record, "lineno", caller_info["lineno"])

        message = super().format(record)
        if self._escape_newline is not None:
            message = self._escape_newline.join(message.splitlines())

        if callable(self._color_fn):
            level_color = self._color_fn(record.levelno)
            message = f"{level_color}{message}{Colors.RESET.value}"

        if self._cipher and message:
            message = self._cipher.encrypt(message, record.levelname)
        return message

    @staticmethod
    def default_color_fn(level: int) -> str:
        c = Colors.DEFAULT
        if level == logging.CRITICAL:
            c = Colors.RED_BG
        elif level == logging.ERROR:
            c = Colors.RED
        elif level == logging.WARNING:
            c = Colors.YELLOW
        elif level == logging.INFO:
            c = Colors.GREEN
        elif level == logging.DEBUG:
            c = Colors.ORANGE
        return c.value

import logging
import logging.handlers
from typing import TYPE_CHECKING, Any, Optional, TextIO, Union

# fixed in 3.11 https://github.com/python/cpython/pull/92129
if TYPE_CHECKING:
    StreamHandler = logging.StreamHandler[TextIO]
else:
    StreamHandler = logging.StreamHandler


class ConsoleHandler(StreamHandler):
    def __init__(
        self,
        stream: Optional[TextIO] = None,
        *,
        formatter: Optional[Union[logging.Formatter, str]] = None,
        level: Optional[int] = None,
    ) -> None:
        super().__init__(stream)
        if isinstance(formatter, logging.Formatter):
            self.setFormatter(formatter)
        elif isinstance(formatter, str):
            self.setFormatter(logging.Formatter(formatter))
        if level is not None:
            self.setLevel(level)


class FileHandler(logging.FileHandler):
    def __init__(
        self,
        filename: str,
        encoding: str = "utf-8",
        *,
        formatter: Optional[Union[logging.Formatter, str]] = None,
        level: Optional[int] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(filename, encoding=encoding, **kwargs)
        if isinstance(formatter, logging.Formatter):
            self.setFormatter(formatter)
        elif isinstance(formatter, str):
            self.setFormatter(logging.Formatter(formatter))
        if level is not None:
            self.setLevel(level)


class TimedRotatingFileHandler(logging.handlers.TimedRotatingFileHandler):
    def __init__(
        self,
        filename: str,
        when: str = "D",
        backupCount: int = 7,
        encoding: str = "utf-8",
        *,
        formatter: Optional[Union[logging.Formatter, str]] = None,
        level: Optional[int] = None,
        **kwargs: Any,
    ):
        super().__init__(
            filename,
            when=when,
            backupCount=backupCount,
            encoding=encoding,
            **kwargs,
        )
        if isinstance(formatter, logging.Formatter):
            self.setFormatter(formatter)
        elif isinstance(formatter, str):
            self.setFormatter(logging.Formatter(formatter))
        if level is not None:
            self.setLevel(level)

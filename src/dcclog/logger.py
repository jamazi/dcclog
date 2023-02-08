import logging
from typing import Iterable, Optional, Union

from dcclog.cipher import Cipher
from dcclog.formatters import Formatter

_default_handlers: list[logging.Handler] = []


def getLogger(
    name: Optional[str] = None,
    *,
    level: Union[str, int] = logging.DEBUG,
    handlers: Union[Iterable[logging.Handler], logging.Handler, None] = None,
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.propagate = False
    logger.setLevel(level)
    if isinstance(handlers, logging.Handler):
        logger.addHandler(handlers)
    elif isinstance(handlers, Iterable):
        for hdlr in handlers:
            logger.addHandler(hdlr)
    if not logger.hasHandlers():
        for h in _default_handlers:
            logger.addHandler(h)
    return logger


def default_config(
    level: int = logging.NOTSET,
    color: bool = True,
    filename: Optional[str] = None,
    file_level: int = logging.NOTSET,
    cipher: Optional[Cipher] = None,
) -> None:
    if not _default_handlers:
        console_hdlr = logging.StreamHandler()
        console_hdlr.setLevel(level)
        console_hdlr.setFormatter(Formatter(color=color))
        _default_handlers.append(console_hdlr)
        if filename:
            file_hdlr = logging.FileHandler(filename)
            file_hdlr.setLevel(file_level)
            file_hdlr.setFormatter(Formatter(cipher=cipher))
            _default_handlers.append(file_hdlr)

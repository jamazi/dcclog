from enum import Enum


class Colors(Enum):
    BLACK = "\033[1;30m"
    RED = "\033[1;31m"
    RED_BG = "\033[1;41m"
    GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    ORANGE = "\033[38;5;214m"
    BLUE = "\033[1;34m"
    MAGENTA = "\033[1;35m"
    CYAN = "\033[1;36m"
    WHITE = "\033[1;37m"
    DEFAULT = "\033[1;39m"

    RESET = "\033[0m"

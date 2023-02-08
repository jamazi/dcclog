from typing import Iterator, Optional

from dcclog.cipher import Cipher


def read_log(logfile: str, cipher: Optional[Cipher] = None) -> Iterator[str]:
    with open(logfile, encoding="utf8") as file:
        for message in file:
            message = message.rstrip("\n")
            if message:
                if cipher:
                    try:
                        yield cipher.decrypt(message)
                    except ValueError:
                        pass
                else:
                    yield message

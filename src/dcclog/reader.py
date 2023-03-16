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


def main() -> int:
    import argparse
    from pathlib import Path

    def _parse_log_files(
        keyfile: Path, logs_dir: Path, filter_: str, expand: bool
    ) -> None:
        from dcclog.cipher.rsa import RSAEncryption

        cipher = RSAEncryption(keyfile.as_posix())
        for file in logs_dir.glob("*.log*"):
            print(f"\n============ LOG FILE {file.name} ============\n")
            for log in read_log(file.as_posix(), cipher):
                if filter_ in log:
                    print(log.replace("\\n\t", "\n") if expand else log)

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-k", "--key", required=True, type=Path)
    arg_parser.add_argument("-l", "--logs-dir", required=True, type=Path)
    arg_parser.add_argument("-f", "--filter", default="", type=str)
    arg_parser.add_argument(
        "--expand", default=True, action=argparse.BooleanOptionalAction
    )
    args = arg_parser.parse_args()
    _parse_log_files(
        args.key.resolve(), args.logs_dir.resolve(), args.filter, args.expand
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from dataclasses import dataclass
from typing import Protocol

from dcclog.utils import b2str, from_json, str2b, to_json


@dataclass
class CipherMessage:
    nonce: bytes
    tag: bytes
    ciphertext: bytes
    extra: bytes
    version: str = ""
    cipher: str = ""

    def encode(self) -> str:
        d = {
            "nonce": b2str(self.nonce),
            "tag": b2str(self.tag),
            "ciphertext": b2str(self.ciphertext),
            "extra": b2str(self.extra),
        }
        return b2str(to_json(d))

    @classmethod
    def decode(cls, s: str) -> "CipherMessage":
        try:
            _, version_and_type, encoded_message = s.split(" :: ")
            msg_cipher, msg_version = version_and_type.strip().split("-")
            decoded_message = from_json(str2b(encoded_message))
            if isinstance(decoded_message, dict):
                d: dict[str, bytes] = {}
                for k, v in decoded_message.items():
                    if not (isinstance(k, str) and isinstance(v, str)):
                        raise ValueError("Invalid ciphertext.")
                    d[k] = str2b(v)
                return cls(version=msg_version, cipher=msg_cipher, **d)
        except Exception as exc:
            raise ValueError("Invalid log format.") from exc
        raise ValueError("Invalid log format.")


class Cipher(Protocol):
    def encrypt(self, plaintext: str, level: str) -> str:
        ...

    def decrypt(self, ciphertext: str) -> str:
        ...


class RawCipher(Protocol):
    @staticmethod
    def encrypt_data(key: bytes, data: bytes, extra: bytes) -> CipherMessage:
        ...

    @staticmethod
    def decrypt_data(key: bytes, data: CipherMessage) -> bytes:
        ...

    @staticmethod
    def cipher() -> str:
        ...

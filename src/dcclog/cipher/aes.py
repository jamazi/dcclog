from typing import Optional

from Crypto.Cipher import AES
from Crypto.Hash import SHA512
from Crypto.Protocol.KDF import PBKDF2

from dcclog.cipher import CipherMessage

LOG_VER = 1
LOG_CIPHER = "AES"


class AESEncryption:
    KEYSIZE = 32
    ITER_COUNT = 100000

    def __init__(self, password: str, salt: Optional[bytes] = None) -> None:
        if salt is None:
            salt = SHA512.new(password.encode()).digest()
        self._key = PBKDF2(
            password=password,
            salt=salt,
            dkLen=self.KEYSIZE,
            count=self.ITER_COUNT,
            hmac_hash_module=SHA512,
        )
        self._salt = salt

    def encrypt(self, plaintext: str, level: str) -> str:
        message = self.encrypt_data(
            self._key, plaintext.encode(), level.encode()
        )

        return f"{level: <8} :: {LOG_CIPHER}-{LOG_VER} :: {message.encode()}"

    def decrypt(self, ciphertext: str) -> str:
        message = CipherMessage.decode(ciphertext)
        if message.cipher != LOG_CIPHER or int(message.version) > LOG_VER:
            raise ValueError("Unsupported log format.")
        try:
            return self.decrypt_data(self._key, message).decode()
        except (ValueError, KeyError) as key_error:
            raise ValueError("Invalid ciphertext or password.") from key_error

    @staticmethod
    def encrypt_data(key: bytes, data: bytes, extra: bytes) -> CipherMessage:
        cipher = AES.new(key, AES.MODE_GCM)
        cipher.update(extra)
        ciphertext, tag = cipher.encrypt_and_digest(data)
        return CipherMessage(
            nonce=cipher.nonce,
            tag=tag,
            ciphertext=ciphertext,
            extra=extra,
        )

    @staticmethod
    def decrypt_data(key: bytes, data: CipherMessage) -> bytes:
        cipher = AES.new(key, AES.MODE_GCM, nonce=data.nonce)
        cipher.update(data.extra)
        return cipher.decrypt_and_verify(data.ciphertext, data.tag)

    @staticmethod
    def cipher() -> str:
        return LOG_CIPHER

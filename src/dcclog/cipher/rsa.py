from typing import Optional, Type, Union

from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA512
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes

from dcclog.cipher import CipherMessage, RawCipher

LOG_VER = 1
LOG_CIPHER = "RSA"


def _default_cipher() -> Type[RawCipher]:
    from dcclog.cipher import chacha

    return chacha.ChachaEncryption


class RSAEncryption:
    MINIMUM_KEYSIZE = 2048
    KEYSIZE = 32

    def __init__(
        self,
        key: Union[str, RSA.RsaKey],
        password: Optional[str] = None,
        cipher: Type[RawCipher] = _default_cipher(),
    ) -> None:
        if isinstance(key, RSA.RsaKey):
            rsa_key = key
        else:
            with open(key, "rb") as f:
                rsa_key = RSA.import_key(
                    f.read(),
                    passphrase=password,
                )
        if rsa_key.size_in_bits() < self.MINIMUM_KEYSIZE:
            raise ValueError("Key size is very short.")

        self._rsa_cipher = PKCS1_OAEP.new(rsa_key, hashAlgo=SHA512)

        self._key = get_random_bytes(self.KEYSIZE)
        self._enc_key = self._rsa_cipher.encrypt(self._key)

        self._cipher = cipher

    def encrypt(self, plaintext: str, level: str) -> str:
        message = self._cipher.encrypt_data(
            self._key, plaintext.encode(), self._enc_key
        )

        return (
            f"{level: <8} :: "
            f"{LOG_CIPHER}+{self._cipher.cipher()}-{LOG_VER} :: "
            f"{message.encode()}"
        )

    def decrypt(self, ciphertext: str) -> str:
        message = CipherMessage.decode(ciphertext)
        session_key = self._rsa_cipher.decrypt(message.extra)
        if (
            int(message.version) > LOG_VER
            or message.cipher != f"{LOG_CIPHER}+{self._cipher.cipher()}"
        ):
            raise ValueError("Unsupported log format.")
        try:
            return self._cipher.decrypt_data(session_key, message).decode()
        except (ValueError, KeyError) as key_error:
            raise ValueError("Invalid ciphertext or keyfile.") from key_error

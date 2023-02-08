import pytest
from Crypto.PublicKey import RSA

from dcclog.cipher.rsa import RSAEncryption

plaintext = "Sensitive plain information."
key1 = RSA.generate(2048)
key2 = RSA.generate(2048)


def test_rsa_correct_key() -> None:
    rsa = RSAEncryption(key1)
    ciphertext = rsa.encrypt(plaintext, "DEBUG")

    assert plaintext == rsa.decrypt(ciphertext)

    with pytest.raises(ValueError):
        rsa.decrypt(ciphertext + "INVALID")


def test_rsa_invalid_key() -> None:
    ciphertext = RSAEncryption(key1).encrypt(plaintext, "DEBUG")
    with pytest.raises(ValueError):
        RSAEncryption(key2).decrypt(ciphertext)

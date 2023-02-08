import pytest

from dcclog.cipher.aes import AESEncryption

plaintext = "Sensitive plain information."


def test_aes_correct_password() -> None:
    aes = AESEncryption("password")
    ciphertext = aes.encrypt(plaintext, "DEBUG")

    assert plaintext == aes.decrypt(ciphertext)

    with pytest.raises(ValueError):
        aes.decrypt(ciphertext + "INVALID")


def test_aes_invalid_password() -> None:
    ciphertext = AESEncryption("password").encrypt(plaintext, "DEBUG")
    with pytest.raises(ValueError):
        AESEncryption("invalid password").decrypt(ciphertext)

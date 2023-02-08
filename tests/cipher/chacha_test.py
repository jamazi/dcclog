import pytest

from dcclog.cipher.chacha import ChachaEncryption

plaintext = "Sensitive plain information."


def test_chacha_correct_password() -> None:
    chacha = ChachaEncryption("password")
    ciphertext = chacha.encrypt(plaintext, "DEBUG")

    assert plaintext == chacha.decrypt(ciphertext)

    with pytest.raises(ValueError):
        chacha.decrypt(ciphertext + "INVALID")


def test_chacha_invalid_password() -> None:
    ciphertext = ChachaEncryption("password").encrypt(plaintext, "DEBUG")
    with pytest.raises(ValueError):
        ChachaEncryption("invalid password").decrypt(ciphertext)

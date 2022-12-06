from base64 import b64encode

import pytest
from pydantic.errors import BytesError

from monkeytypes.types.b64_bytes import b64_bytes_validator

BYTES = b"random bytes"


def test_b64_bytes_validator__bytes():
    fake_bytes = BYTES
    assert b64_bytes_validator(fake_bytes) == fake_bytes


def test_b64_bytes_validator__bytearray():
    fake_byte_array = bytearray(BYTES)
    assert b64_bytes_validator(fake_byte_array) == fake_byte_array


def test_b64_bytes_validator__b64_string():
    fake_b64_string = b64encode(BYTES).decode()
    assert b64_bytes_validator(fake_b64_string) == BYTES


def test_64_bytes_validator__bad_b64():
    fake_b64_string = "abc"
    with pytest.raises(BytesError):
        b64_bytes_validator(fake_b64_string)


def test_64_bytes_validator__not_bytes():
    bad_input = 134567

    with pytest.raises(BytesError):
        b64_bytes_validator(bad_input)

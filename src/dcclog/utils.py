import base64
from json import dumps, loads
from typing import Any, Union


def str2b(b: Union[str, bytes]) -> bytes:
    return base64.b85decode(b)


def b2str(b: Union[str, bytes]) -> str:
    if isinstance(b, str):
        b = b.encode()
    return base64.b85encode(b).decode()


def from_json(s: Union[str, bytes, bytearray]) -> Any:
    def json_decoder(obj: dict[str, Any]) -> Any:
        if ":bytes" in obj:
            return str2b(obj[":bytes"])
        return obj

    return loads(s, object_hook=json_decoder)


def to_json(obj: Any) -> str:
    def json_encoder(v: Any) -> dict[str, str]:
        if isinstance(v, bytes):
            return {":bytes": b2str(v)}
        raise TypeError(repr(v) + " is not JSON serializable")

    return dumps(obj, separators=(",", ":"), default=json_encoder)

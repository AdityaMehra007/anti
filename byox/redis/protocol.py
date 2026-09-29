"""
RESP2 Protocol Serializer and Deserializer.
"""

from typing import Any, Tuple, Optional, List

class RESPSerializer:
    @staticmethod
    def simple_string(s: str) -> bytes:
        return f"+{s}\r\n".encode("utf-8")

    @staticmethod
    def error(msg: str) -> bytes:
        return f"-{msg}\r\n".encode("utf-8")

    @staticmethod
    def integer(n: int) -> bytes:
        return f":{n}\r\n".encode("ascii")

    @staticmethod
    def bulk_string(data: Optional[bytes | str]) -> bytes:
        if data is None:
            return b"$-1\r\n"
        if isinstance(data, str):
            data = data.encode("utf-8")
        return f"${len(data)}\r\n".encode("ascii") + data + b"\r\n"

    @classmethod
    def array(cls, items: Optional[List[Any]]) -> bytes:
        if items is None:
            return b"*-1\r\n"
        parts = [f"*{len(items)}\r\n".encode("ascii")]
        for item in items:
            parts.append(cls.encode(item))
        return b"".join(parts)

    @classmethod
    def encode(cls, val: Any) -> bytes:
        if val is None:
            return cls.bulk_string(None)
        if isinstance(val, bool):
            return cls.integer(1 if val else 0)
        if isinstance(val, int):
            return cls.integer(val)
        if isinstance(val, bytes):
            return cls.bulk_string(val)
        if isinstance(val, str):
            # If string starts with standard OK/PONG or status, format as simple string or bulk string
            if val in ("OK", "PONG", "QUEUED"):
                return cls.simple_string(val)
            return cls.bulk_string(val.encode("utf-8"))
        if isinstance(val, Exception):
            return cls.error(str(val))
        if isinstance(val, (list, tuple)):
            return cls.array(val)
        return cls.bulk_string(str(val).encode("utf-8"))


class RESPParser:
    @classmethod
    def parse(cls, buf: bytes) -> Tuple[Any, int]:
        """
        Parses the first complete RESP value from buf.
        Returns (parsed_value, bytes_consumed).
        Raises IncompleteBufferError if buffer contains partial data.
        """
        if not buf:
            raise ValueError("Empty buffer")

        prefix = buf[0:1]
        crlf_pos = buf.find(b"\r\n")
        if crlf_pos == -1:
            raise ValueError("Incomplete line: missing CRLF")

        line = buf[1:crlf_pos]

        if prefix == b"+":
            return line.decode("utf-8"), crlf_pos + 2

        elif prefix == b"-":
            return Exception(line.decode("utf-8")), crlf_pos + 2

        elif prefix == b":":
            return int(line), crlf_pos + 2

        elif prefix == b"$":
            length = int(line)
            if length == -1:
                return None, crlf_pos + 2
            start = crlf_pos + 2
            end = start + length
            if len(buf) < end + 2:
                raise ValueError("Incomplete bulk string payload")
            if buf[end:end+2] != b"\r\n":
                raise ValueError("Malformed bulk string trailing CRLF")
            return buf[start:end], end + 2

        elif prefix == b"*":
            num_elements = int(line)
            if num_elements == -1:
                return None, crlf_pos + 2
            elements = []
            offset = crlf_pos + 2
            for _ in range(num_elements):
                elem, consumed = cls.parse(buf[offset:])
                elements.append(elem)
                offset += consumed
            return elements, offset

        else:
            # Inline command fallback (e.g. plain text "PING\r\n")
            parts = line.decode("utf-8").split(" ")
            return [p.encode("utf-8") for p in parts if p], crlf_pos + 2

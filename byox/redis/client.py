"""
Lightweight Redis RESP Client.
"""

import socket
from typing import Any
from byox.redis.protocol import RESPParser, RESPSerializer

class RedisClient:
    def __init__(self, host: str = "127.0.0.1", port: int = 6379, timeout: float = 5.0):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(timeout)
        self.sock.connect((self.host, self.port))
        self._buf = b""

    def execute(self, *args: Any) -> Any:
        payload = RESPSerializer.encode(list(args))
        self.sock.sendall(payload)

        while True:
            try:
                val, consumed = RESPParser.parse(self._buf)
                self._buf = self._buf[consumed:]
                if isinstance(val, Exception):
                    raise val
                return val
            except ValueError:
                # Need more data
                chunk = self.sock.recv(4096)
                if not chunk:
                    raise ConnectionResetError("Server closed connection")
                self._buf += chunk

    def close(self):
        try:
            self.sock.close()
        except OSError:
            pass

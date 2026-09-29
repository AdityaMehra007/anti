"""
Redis RESP TCP Socket Server.
"""

import socket
import threading
from typing import Optional
from byox.redis.protocol import RESPParser, RESPSerializer
from byox.redis.store import DataStore

class RedisServer:
    def __init__(self, host: str = "127.0.0.1", port: int = 6379):
        self.host = host
        self.port = port
        self.store = DataStore()
        self._server_sock: Optional[socket.socket] = None
        self._running = False
        self._thread: Optional[threading.Thread] = None

    def start(self, blocking: bool = False):
        self._server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_sock.bind((self.host, self.port))
        self.port = self._server_sock.getsockname()[1]
        self._server_sock.listen(128)
        self._running = True

        if blocking:
            self._serve()
        else:
            self._thread = threading.Thread(target=self._serve, daemon=True)
            self._thread.start()

    def _serve(self):
        while self._running:
            try:
                conn, addr = self._server_sock.accept()
            except (OSError, socket.error):
                break
            client_thread = threading.Thread(target=self._handle_client, args=(conn,), daemon=True)
            client_thread.start()

    def _handle_client(self, conn: socket.socket):
        buf = b""
        with conn:
            while self._running:
                try:
                    data = conn.recv(4096)
                    if not data:
                        break
                    buf += data
                    while buf:
                        try:
                            parsed, consumed = RESPParser.parse(buf)
                            buf = buf[consumed:]
                        except ValueError:
                            # Incomplete buffer, await more data
                            break

                        if isinstance(parsed, list) and parsed:
                            cmd = parsed[0]
                            args = parsed[1:]
                            result = self.store.execute(cmd, *args)
                        else:
                            result = Exception("ERR unknown request format")

                        conn.sendall(RESPSerializer.encode(result))
                except (ConnectionResetError, BrokenPipeError, socket.error):
                    break

    def stop(self):
        self._running = False
        if self._server_sock:
            try:
                self._server_sock.close()
            except OSError:
                pass
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=1.0)

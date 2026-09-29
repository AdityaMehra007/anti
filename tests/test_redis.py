import time
import socket
import unittest
from byox.redis.protocol import RESPParser, RESPSerializer
from byox.redis.store import DataStore
from byox.redis.server import RedisServer
from byox.redis.client import RedisClient

class TestRedis(unittest.TestCase):
    def test_resp_serialization(self):
        # Simple String
        self.assertEqual(RESPSerializer.simple_string("OK"), b"+OK\r\n")
        # Error
        self.assertEqual(RESPSerializer.error("Error msg"), b"-Error msg\r\n")
        # Integer
        self.assertEqual(RESPSerializer.integer(100), b":100\r\n")
        # Bulk String
        self.assertEqual(RESPSerializer.bulk_string(b"foobar"), b"$6\r\nfoobar\r\n")
        self.assertEqual(RESPSerializer.bulk_string(None), b"$-1\r\n")
        # Array
        self.assertEqual(
            RESPSerializer.array([b"PING"]),
            b"*1\r\n$4\r\nPING\r\n"
        )

    def test_resp_parsing(self):
        # Simple string
        val, consumed = RESPParser.parse(b"+PONG\r\n")
        self.assertEqual(val, "PONG")
        self.assertEqual(consumed, 7)

        # Integer
        val, consumed = RESPParser.parse(b":42\r\n")
        self.assertEqual(val, 42)

        # Bulk string
        val, consumed = RESPParser.parse(b"$5\r\nhello\r\n")
        self.assertEqual(val, b"hello")

        # Null bulk string
        val, consumed = RESPParser.parse(b"$-1\r\n")
        self.assertIsNone(val)

        # Array
        val, consumed = RESPParser.parse(b"*2\r\n$4\r\nECHO\r\n$5\r\nworld\r\n")
        self.assertEqual(val, [b"ECHO", b"world"])

    def test_datastore_operations(self):
        store = DataStore()
        
        # Strings
        self.assertEqual(store.execute("SET", "mykey", "hello"), "OK")
        self.assertEqual(store.execute("GET", "mykey"), b"hello")
        
        # Expiration
        store.execute("SET", "temp", "val", "PX", "50")  # 50 ms
        self.assertEqual(store.execute("GET", "temp"), b"val")
        time.sleep(0.06)
        self.assertIsNone(store.execute("GET", "temp"))

        # INCR / DECR
        self.assertEqual(store.execute("SET", "counter", "10"), "OK")
        self.assertEqual(store.execute("INCR", "counter"), 11)
        self.assertEqual(store.execute("DECR", "counter"), 10)

        # Lists
        self.assertEqual(store.execute("RPUSH", "mylist", "a"), 1)
        self.assertEqual(store.execute("RPUSH", "mylist", "b"), 2)
        self.assertEqual(store.execute("LPUSH", "mylist", "first"), 3)
        self.assertEqual(store.execute("LRANGE", "mylist", "0", "-1"), [b"first", b"a", b"b"])
        self.assertEqual(store.execute("LPOP", "mylist"), b"first")

        # Hashes
        self.assertEqual(store.execute("HSET", "user:1", "name", "Alice", "role", "admin"), 2)
        self.assertEqual(store.execute("HGET", "user:1", "name"), b"Alice")
        hdict = store.execute("HGETALL", "user:1")
        self.assertEqual(hdict, [b"name", b"Alice", b"role", b"admin"])

    def test_server_and_client_integration(self):
        server = RedisServer(host="127.0.0.1", port=0)
        server.start()
        port = server.port
        self.assertGreater(port, 0)

        try:
            client = RedisClient(host="127.0.0.1", port=port)
            self.assertEqual(client.execute("PING"), "PONG")
            self.assertEqual(client.execute("ECHO", "hello client"), b"hello client")
            self.assertEqual(client.execute("SET", "k1", "v1"), "OK")
            self.assertEqual(client.execute("GET", "k1"), b"v1")
            client.close()
        finally:
            server.stop()

if __name__ == "__main__":
    unittest.main()

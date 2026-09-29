"""
Redis In-Memory Data Store with TTL Expiration and Command Handlers.
"""

import time
from typing import Any, Dict, List, Optional, Tuple

class DataStore:
    def __init__(self):
        self._strings: Dict[str, bytes] = {}
        self._lists: Dict[str, List[bytes]] = {}
        self._hashes: Dict[str, Dict[str, bytes]] = {}
        self._expires: Dict[str, float] = {}  # key -> monotonic expire time (seconds)

    def _is_expired(self, key: str) -> bool:
        if key in self._expires:
            if time.monotonic() > self._expires[key]:
                self._delete_internal(key)
                return True
        return False

    def _delete_internal(self, key: str):
        self._strings.pop(key, None)
        self._lists.pop(key, None)
        self._hashes.pop(key, None)
        self._expires.pop(key, None)

    def execute(self, cmd_name: str | bytes, *args: Any) -> Any:
        if isinstance(cmd_name, bytes):
            cmd_name = cmd_name.decode("utf-8")
        cmd_name = cmd_name.upper()

        # Normalize args to strings/bytes
        str_args: List[str] = []
        raw_args: List[bytes] = []
        for a in args:
            if isinstance(a, bytes):
                raw_args.append(a)
                str_args.append(a.decode("utf-8", errors="replace"))
            else:
                s = str(a)
                str_args.append(s)
                raw_args.append(s.encode("utf-8"))

        handler = getattr(self, f"cmd_{cmd_name.lower()}", None)
        if handler is None:
            return Exception(f"ERR unknown command '{cmd_name}'")
        return handler(str_args, raw_args)

    def cmd_ping(self, str_args: List[str], raw_args: List[bytes]) -> Any:
        if raw_args:
            return raw_args[0]
        return "PONG"

    def cmd_echo(self, str_args: List[str], raw_args: List[bytes]) -> Any:
        if not raw_args:
            return Exception("ERR wrong number of arguments for 'echo' command")
        return raw_args[0]

    def cmd_set(self, str_args: List[str], raw_args: List[bytes]) -> Any:
        if len(str_args) < 2:
            return Exception("ERR wrong number of arguments for 'set' command")
        key = str_args[0]
        val = raw_args[1]
        self._delete_internal(key)
        self._strings[key] = val

        # Handle options (PX milliseconds or EX seconds)
        idx = 2
        while idx < len(str_args):
            opt = str_args[idx].upper()
            if opt == "PX" and idx + 1 < len(str_args):
                ms = float(str_args[idx + 1])
                self._expires[key] = time.monotonic() + (ms / 1000.0)
                idx += 2
            elif opt == "EX" and idx + 1 < len(str_args):
                sec = float(str_args[idx + 1])
                self._expires[key] = time.monotonic() + sec
                idx += 2
            else:
                idx += 1
        return "OK"

    def cmd_get(self, str_args: List[str], raw_args: List[bytes]) -> Any:
        if len(str_args) != 1:
            return Exception("ERR wrong number of arguments for 'get' command")
        key = str_args[0]
        if self._is_expired(key) or key not in self._strings:
            return None
        return self._strings[key]

    def cmd_del(self, str_args: List[str], raw_args: List[bytes]) -> Any:
        count = 0
        for key in str_args:
            if not self._is_expired(key) and (key in self._strings or key in self._lists or key in self._hashes):
                self._delete_internal(key)
                count += 1
        return count

    def cmd_exists(self, str_args: List[str], raw_args: List[bytes]) -> Any:
        count = 0
        for key in str_args:
            if not self._is_expired(key) and (key in self._strings or key in self._lists or key in self._hashes):
                count += 1
        return count

    def cmd_incr(self, str_args: List[str], raw_args: List[bytes]) -> Any:
        if len(str_args) != 1:
            return Exception("ERR wrong number of arguments for 'incr' command")
        return self._incrby(str_args[0], 1)

    def cmd_decr(self, str_args: List[str], raw_args: List[bytes]) -> Any:
        if len(str_args) != 1:
            return Exception("ERR wrong number of arguments for 'decr' command")
        return self._incrby(str_args[0], -1)

    def _incrby(self, key: str, amount: int) -> Any:
        if self._is_expired(key) or key not in self._strings:
            self._strings[key] = str(amount).encode("ascii")
            return amount
        try:
            curr = int(self._strings[key].decode("ascii"))
            curr += amount
            self._strings[key] = str(curr).encode("ascii")
            return curr
        except ValueError:
            return Exception("ERR value is not an integer or out of range")

    def cmd_rpush(self, str_args: List[str], raw_args: List[bytes]) -> Any:
        if len(str_args) < 2:
            return Exception("ERR wrong number of arguments for 'rpush' command")
        key = str_args[0]
        if self._is_expired(key):
            self._delete_internal(key)
        lst = self._lists.setdefault(key, [])
        for val in raw_args[1:]:
            lst.append(val)
        return len(lst)

    def cmd_lpush(self, str_args: List[str], raw_args: List[bytes]) -> Any:
        if len(str_args) < 2:
            return Exception("ERR wrong number of arguments for 'lpush' command")
        key = str_args[0]
        if self._is_expired(key):
            self._delete_internal(key)
        lst = self._lists.setdefault(key, [])
        for val in raw_args[1:]:
            lst.insert(0, val)
        return len(lst)

    def cmd_lpop(self, str_args: List[str], raw_args: List[bytes]) -> Any:
        if not str_args:
            return Exception("ERR wrong number of arguments for 'lpop' command")
        key = str_args[0]
        if self._is_expired(key) or key not in self._lists or not self._lists[key]:
            return None
        return self._lists[key].pop(0)

    def cmd_rpop(self, str_args: List[str], raw_args: List[bytes]) -> Any:
        if not str_args:
            return Exception("ERR wrong number of arguments for 'rpop' command")
        key = str_args[0]
        if self._is_expired(key) or key not in self._lists or not self._lists[key]:
            return None
        return self._lists[key].pop()

    def cmd_llen(self, str_args: List[str], raw_args: List[bytes]) -> Any:
        key = str_args[0]
        if self._is_expired(key) or key not in self._lists:
            return 0
        return len(self._lists[key])

    def cmd_lrange(self, str_args: List[str], raw_args: List[bytes]) -> Any:
        if len(str_args) != 3:
            return Exception("ERR wrong number of arguments for 'lrange' command")
        key = str_args[0]
        start = int(str_args[1])
        stop = int(str_args[2])
        if self._is_expired(key) or key not in self._lists:
            return []
        lst = self._lists[key]
        n = len(lst)
        if start < 0:
            start = max(0, n + start)
        if stop < 0:
            stop = n + stop
        return lst[start : stop + 1]

    def cmd_hset(self, str_args: List[str], raw_args: List[bytes]) -> Any:
        if len(str_args) < 3 or (len(str_args) - 1) % 2 != 0:
            return Exception("ERR wrong number of arguments for 'hset' command")
        key = str_args[0]
        if self._is_expired(key):
            self._delete_internal(key)
        h = self._hashes.setdefault(key, {})
        added = 0
        for i in range(1, len(str_args), 2):
            field = str_args[i]
            val = raw_args[i + 1]
            if field not in h:
                added += 1
            h[field] = val
        return added

    def cmd_hget(self, str_args: List[str], raw_args: List[bytes]) -> Any:
        if len(str_args) != 2:
            return Exception("ERR wrong number of arguments for 'hget' command")
        key, field = str_args[0], str_args[1]
        if self._is_expired(key) or key not in self._hashes:
            return None
        return self._hashes[key].get(field)

    def cmd_hgetall(self, str_args: List[str], raw_args: List[bytes]) -> Any:
        if len(str_args) != 1:
            return Exception("ERR wrong number of arguments for 'hgetall' command")
        key = str_args[0]
        if self._is_expired(key) or key not in self._hashes:
            return []
        res = []
        for f, v in self._hashes[key].items():
            res.append(f.encode("utf-8"))
            res.append(v)
        return res

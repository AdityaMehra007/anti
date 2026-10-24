"""
ApexAgentic Runtime - Stateful SQLite Checkpointer.
Enables time-travel rollback, crash recovery, and state resumption for long-running agent workflows.
"""

import json
import sqlite3
import time
from typing import Any, Dict, List, Optional


class AgentCheckpointer:
    """
    Saves immutable state snapshots after each autonomous agent thought/action step.
    """

    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        if self.db_path == ":memory:":
            self._conn = sqlite3.connect("file:checkpoint_mem?mode=memory&cache=shared", uri=True, check_same_thread=False)
        else:
            self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._init_db()

    def _init_db(self) -> None:
        with self._conn:
            self._conn.execute("""
                CREATE TABLE IF NOT EXISTS agent_checkpoints (
                    session_id TEXT NOT NULL,
                    step_index INTEGER NOT NULL,
                    state_json TEXT NOT NULL,
                    timestamp REAL NOT NULL,
                    PRIMARY KEY (session_id, step_index)
                );
            """)

    def save_checkpoint(self, session_id: str, step_index: int, state: Dict[str, Any]) -> None:
        state_serialized = json.dumps(state, default=str)
        now = time.time()
        with self._conn:
            self._conn.execute(
                """
                INSERT OR REPLACE INTO agent_checkpoints
                (session_id, step_index, state_json, timestamp)
                VALUES (?, ?, ?, ?)
                """,
                (session_id, step_index, state_serialized, now)
            )

    def load_latest(self, session_id: str) -> Optional[Dict[str, Any]]:
        cursor = self._conn.cursor()
        cursor.execute(
            """
            SELECT state_json FROM agent_checkpoints
            WHERE session_id = ?
            ORDER BY step_index DESC LIMIT 1
            """,
            (session_id,)
        )
        row = cursor.fetchone()
        return json.loads(row[0]) if row else None

    def rollback_to(self, session_id: str, target_step_index: int) -> Optional[Dict[str, Any]]:
        cursor = self._conn.cursor()
        cursor.execute(
            """
            SELECT state_json FROM agent_checkpoints
            WHERE session_id = ? AND step_index = ?
            """,
            (session_id, target_step_index)
        )
        row = cursor.fetchone()
        if row:
            # Prune subsequent forward checkpoints
            with self._conn:
                self._conn.execute(
                    "DELETE FROM agent_checkpoints WHERE session_id = ? AND step_index > ?",
                    (session_id, target_step_index)
                )
            return json.loads(row[0])
        return None

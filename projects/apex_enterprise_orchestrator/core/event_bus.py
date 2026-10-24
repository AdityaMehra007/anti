"""
ApexFlow Enterprise Core - Async Event Bus & Dead-Letter Queue (DLQ).
Handles decoupled domain event routing, fan-out distribution, and failure quarantine.
"""

import asyncio
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import IntEnum
from typing import Any, Callable, Coroutine, Dict, List, Optional
import uuid


class EventPriority(IntEnum):
    LOW = 30
    NORMAL = 20
    HIGH = 10
    CRITICAL = 0


@dataclass
class DomainEvent:
    event_type: str
    payload: Dict[str, Any]
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    priority: EventPriority = EventPriority.NORMAL
    trace_id: Optional[str] = None


@dataclass
class FailedEventRecord:
    event: DomainEvent
    error_message: str
    attempt_count: int
    failed_at: str


EventHandler = Callable[[DomainEvent], Coroutine[Any, Any, None]]


class AsyncEventBus:
    """
    Decoupled Async Event Bus with Priority Dispatch and Dead-Letter Queue (DLQ).
    """

    def __init__(self, max_retry_attempts: int = 3):
        self._subscribers: Dict[str, List[EventHandler]] = {}
        self._dlq: List[FailedEventRecord] = []
        self._max_retries = max_retry_attempts
        self._queue: asyncio.PriorityQueue = asyncio.PriorityQueue()
        self._is_running = False
        self._worker_task: Optional[asyncio.Task] = None

    def subscribe(self, event_type: str, handler: EventHandler) -> None:
        """Registers an asynchronous handler for a specific event type."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)

    async def publish(self, event: DomainEvent) -> None:
        """Puts event into priority queue ordered by priority level."""
        # Priority queue item: (priority_value, monotonic_counter, event)
        counter = asyncio.get_event_loop().time()
        await self._queue.put((event.priority.value, counter, event))

    async def publish_sync_await(self, event: DomainEvent) -> None:
        """Directly dispatches event to all subscribers without queueing (for critical synchronous paths)."""
        handlers = self._subscribers.get(event.event_type, [])
        for handler in handlers:
            await self._execute_handler_with_retry(handler, event)

    async def _execute_handler_with_retry(self, handler: EventHandler, event: DomainEvent) -> None:
        attempts = 0
        last_error = ""
        while attempts < self._max_retries:
            try:
                attempts += 1
                await handler(event)
                return
            except Exception as exc:
                last_error = str(exc)
                await asyncio.sleep(0.05 * (2 ** (attempts - 1)))  # exponential backoff

        # Quarantined into Dead-Letter Queue
        self._dlq.append(
            FailedEventRecord(
                event=event,
                error_message=last_error,
                attempt_count=attempts,
                failed_at=datetime.now(timezone.utc).isoformat(),
            )
        )

    async def start_worker(self) -> None:
        """Starts background dispatcher loop."""
        self._is_running = True
        self._worker_task = asyncio.create_task(self._process_loop())

    async def stop_worker(self) -> None:
        """Gracefully drains queue and stops worker."""
        self._is_running = False
        if self._worker_task:
            self._worker_task.cancel()
            try:
                await self._worker_task
            except asyncio.CancelledError:
                pass

    async def _process_loop(self) -> None:
        while self._is_running:
            try:
                _, _, event = await self._queue.get()
                handlers = self._subscribers.get(event.event_type, [])
                if handlers:
                    tasks = [self._execute_handler_with_retry(h, event) for h in handlers]
                    await asyncio.gather(*tasks, return_exceptions=True)
                self._queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception:
                await asyncio.sleep(0.1)

    @property
    def dlq(self) -> List[FailedEventRecord]:
        return list(self._dlq)

    def clear_dlq(self) -> None:
        self._dlq.clear()

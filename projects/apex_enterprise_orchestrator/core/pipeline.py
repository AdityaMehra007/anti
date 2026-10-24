"""
ApexFlow Enterprise Core - Async DAG Pipeline Engine.
Executes multi-step complex enterprise workflows with dependency resolution and rollback sagas.
"""

import asyncio
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Coroutine, Dict, List, Optional, Set


class TaskStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"
    ROLLED_BACK = "ROLLED_BACK"


TaskCallable = Callable[[Dict[str, Any]], Coroutine[Any, Any, Any]]
RollbackCallable = Callable[[Dict[str, Any], Any], Coroutine[Any, Any, None]]


@dataclass
class PipelineTask:
    name: str
    action: TaskCallable
    depends_on: List[str] = field(default_factory=list)
    rollback: Optional[RollbackCallable] = None
    status: TaskStatus = TaskStatus.PENDING
    result: Any = None
    error: Optional[str] = None


class PipelineExecutionError(Exception):
    pass


class AsyncPipelineDAG:
    """
    DAG Orchestration Engine with Saga Compensation (Rollback).
    
    Executes tasks in topological levels: tasks with satisfied dependencies execute concurrently.
    If any task fails, executed tasks are rolled back in reverse order.
    """

    def __init__(self, name: str):
        self.name = name
        self.tasks: Dict[str, PipelineTask] = {}

    def add_task(
        self,
        name: str,
        action: TaskCallable,
        depends_on: Optional[List[str]] = None,
        rollback: Optional[RollbackCallable] = None,
    ) -> "AsyncPipelineDAG":
        if name in self.tasks:
            raise ValueError(f"Task '{name}' already exists in pipeline '{self.name}'.")
        self.tasks[name] = PipelineTask(
            name=name,
            action=action,
            depends_on=depends_on or [],
            rollback=rollback,
        )
        return self

    def _validate_dag(self) -> None:
        """Verifies no cycles and all dependencies exist."""
        for name, task in self.tasks.items():
            for dep in task.depends_on:
                if dep not in self.tasks:
                    raise ValueError(f"Task '{name}' depends on non-existent task '{dep}'.")

        # Cycle detection using Kahn's algorithm or DFS
        visited: Set[str] = set()
        rec_stack: Set[str] = set()

        def dfs(node: str) -> None:
            visited.add(node)
            rec_stack.add(node)
            for dep in self.tasks[node].depends_on:
                if dep not in visited:
                    dfs(dep)
                elif dep in rec_stack:
                    raise ValueError(f"Cycle detected in pipeline DAG involving task '{dep}'.")
            rec_stack.remove(node)

        for task_name in self.tasks:
            if task_name not in visited:
                dfs(task_name)

    async def execute(self, initial_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        self._validate_dag()
        context = dict(initial_context or {})
        completed_tasks: List[str] = []

        pending_names = set(self.tasks.keys())

        try:
            while pending_names:
                # Find all tasks ready to run (all dependencies have status == SUCCESS)
                ready_tasks = [
                    self.tasks[name]
                    for name in pending_names
                    if all(self.tasks[dep].status == TaskStatus.SUCCESS for dep in self.tasks[name].depends_on)
                ]

                if not ready_tasks:
                    raise PipelineExecutionError("Deadlock detected in DAG: no tasks ready to execute.")

                # Run ready tasks concurrently
                async def run_single_task(task: PipelineTask) -> None:
                    task.status = TaskStatus.RUNNING
                    try:
                        res = await task.action(context)
                        task.result = res
                        task.status = TaskStatus.SUCCESS
                        context[f"task_{task.name}"] = res
                    except Exception as exc:
                        task.error = str(exc)
                        task.status = TaskStatus.FAILED
                        raise exc

                task_coros = [run_single_task(t) for t in ready_tasks]
                results = await asyncio.gather(*task_coros, return_exceptions=True)

                # Check for failures
                for task, result in zip(ready_tasks, results):
                    if isinstance(result, Exception):
                        raise PipelineExecutionError(
                            f"Pipeline task '{task.name}' failed: {str(result)}"
                        ) from result
                    completed_tasks.append(task.name)
                    pending_names.remove(task.name)

            return context

        except Exception as exc:
            # Trigger saga rollback in reverse order
            await self._execute_rollback(completed_tasks, context)
            raise exc

    async def _execute_rollback(self, executed_task_names: List[str], context: Dict[str, Any]) -> None:
        for name in reversed(executed_task_names):
            task = self.tasks[name]
            if task.rollback:
                try:
                    await task.rollback(context, task.result)
                    task.status = TaskStatus.ROLLED_BACK
                except Exception:
                    # Log but continue rolling back remaining tasks
                    pass

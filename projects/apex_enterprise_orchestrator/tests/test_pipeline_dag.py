"""Tests for ApexFlow Async DAG Pipeline & Rollback Sagas."""

import asyncio
import pytest
from projects.apex_enterprise_orchestrator.core.pipeline import (
    AsyncPipelineDAG,
    PipelineExecutionError,
    TaskStatus,
)


def test_dag_dependency_execution_order():
    async def run():
        dag = AsyncPipelineDAG("settlement_flow")
        execution_order = []

        async def step_fetch(ctx):
            execution_order.append("fetch")
            return {"data": [1, 2, 3]}

        async def step_verify(ctx):
            execution_order.append("verify")
            return True

        async def step_settle(ctx):
            execution_order.append("settle")
            return "SETTLED"

        dag.add_task("fetch", step_fetch)
        dag.add_task("verify", step_verify, depends_on=["fetch"])
        dag.add_task("settle", step_settle, depends_on=["verify"])

        context = await dag.execute()
        assert execution_order == ["fetch", "verify", "settle"]
        assert context["task_settle"] == "SETTLED"

    asyncio.run(run())


def test_dag_triggers_rollback_on_failure():
    async def run():
        dag = AsyncPipelineDAG("faulty_flow")
        rollback_tracker = []

        async def step_reserve_inventory(ctx):
            return "RESERVED"

        async def rollback_inventory(ctx, res):
            rollback_tracker.append("INVENTORY_UNRESERVED")

        async def step_charge_payment(ctx):
            raise RuntimeError("Payment gateway failure")

        dag.add_task("inventory", step_reserve_inventory, rollback=rollback_inventory)
        dag.add_task("payment", step_charge_payment, depends_on=["inventory"])

        with pytest.raises(PipelineExecutionError, match="Payment gateway failure"):
            await dag.execute()

        assert rollback_tracker == ["INVENTORY_UNRESERVED"]
        assert dag.tasks["inventory"].status == TaskStatus.ROLLED_BACK
        assert dag.tasks["payment"].status == TaskStatus.FAILED

    asyncio.run(run())


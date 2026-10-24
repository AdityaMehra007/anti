"""
Tests for ApexAgentic Task Runtime.
Verifies budget governor, safety permissions, epistemic failure memory, and state checkpoints.
"""

import pytest
from pydantic import BaseModel, Field
from projects.apex_agentic_task_runtime.core.agent_runner import DeterministicAgentRuntime
from projects.apex_agentic_task_runtime.guardrails.token_governor import (
    BudgetExceededException,
    TokenBudgetGovernor,
)
from projects.apex_agentic_task_runtime.guardrails.tool_sandbox import (
    ToolPermissionLevel,
    ToolRegistry,
    ToolSecurityException,
)
from projects.apex_agentic_task_runtime.memory.checkpoint import AgentCheckpointer
from projects.apex_agentic_task_runtime.memory.failure_memory import FailedSolutionMemory


class CalculatorInput(BaseModel):
    a: float = Field(..., description="First number")
    b: float = Field(..., description="Second number")


def mock_add(a: float, b: float) -> float:
    return a + b


def mock_delete_database(target: str) -> str:
    return f"Dropped {target}"


def test_token_budget_governor_enforces_limit():
    governor = TokenBudgetGovernor(max_total_tokens=1000, max_cost_usd=0.01)
    
    # Within budget
    cost1 = governor.record_usage(input_tokens=400, output_tokens=100)
    assert cost1 > 0
    assert governor.total_tokens == 500

    # Exceeds token budget
    with pytest.raises(BudgetExceededException, match="Token budget exceeded"):
        governor.record_usage(input_tokens=600, output_tokens=100)


def test_destructive_tool_requires_approval_token():
    registry = ToolRegistry()
    registry.register(
        name="drop_db",
        description="Destructive table dropper",
        func=mock_delete_database,
        permission_level=ToolPermissionLevel.DESTRUCTIVE,
    )

    tool = registry.get("drop_db")

    # Blocked without approval token
    with pytest.raises(ToolSecurityException, match="DESTRUCTIVE action 'drop_db' blocked"):
        tool.execute({"target": "production_users"})

    # Passes with sovereign token
    result = tool.execute({"target": "staging_users"}, approval_token="SOVEREIGN_OVERRIDE_GRANTED")
    assert result == "Dropped staging_users"


def test_failure_memory_intercepts_repeated_errors():
    registry = ToolRegistry()
    
    def faulty_api(endpoint: str):
        if endpoint == "/unauthorized":
            raise PermissionError("403 Forbidden")
        return "200 OK"

    registry.register(name="fetch_api", description="API fetcher", func=faulty_api)
    runtime = DeterministicAgentRuntime(session_id="session_001", tools=registry)

    # 1. First execution fails and logs to FailureMemory
    res1 = runtime.execute_action("fetch_api", {"endpoint": "/unauthorized"})
    assert res1["status"] == "FAILED"
    assert "403 Forbidden" in res1["error"]

    # 2. Second attempt with SAME invalid arguments: Intercepted BEFORE execution!
    res2 = runtime.execute_action("fetch_api", {"endpoint": "/unauthorized"})
    assert res2["status"] == "INTERCEPTED_BY_FAILURE_MEMORY"
    assert "Execution error in fetch_api" in res2["diagnosis"]


def test_checkpoint_time_travel_rollback():
    checkpointer = AgentCheckpointer(db_path=":memory:")
    session = "test_sess"

    checkpointer.save_checkpoint(session, step_index=1, state={"phase": "DISCOVERY"})
    checkpointer.save_checkpoint(session, step_index=2, state={"phase": "BUILDING"})
    checkpointer.save_checkpoint(session, step_index=3, state={"phase": "BROKEN"})

    assert checkpointer.load_latest(session)["phase"] == "BROKEN"

    # Rollback to step 2
    rolled_back = checkpointer.rollback_to(session, target_step_index=2)
    assert rolled_back["phase"] == "BUILDING"
    assert checkpointer.load_latest(session)["phase"] == "BUILDING"

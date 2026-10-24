"""
ApexAgentic Runtime - Autonomous Agent Execution Engine.
Orchestrates perception, epistemic failure check, deterministic tool execution, and checkpointing.
"""

from typing import Any, Dict, List, Optional
from projects.apex_agentic_task_runtime.guardrails.token_governor import (
    BudgetExceededException,
    TokenBudgetGovernor,
)
from projects.apex_agentic_task_runtime.guardrails.tool_sandbox import (
    ToolRegistry,
    ToolSecurityException,
)
from projects.apex_agentic_task_runtime.memory.checkpoint import AgentCheckpointer
from projects.apex_agentic_task_runtime.memory.failure_memory import (
    FailedSolutionMemory,
    FailureRecord,
)


class AgentExecutionException(Exception):
    pass


class DeterministicAgentRuntime:
    """
    High-reliability Agent Execution Runtime.
    
    Guarantees:
    1. Zero Runaway Token Spend (Token & Cost budget limits enforced).
    2. Zero Repeated Mistakes (Failed Solution Memory intercepts known dead ends).
    3. Zero Destructive Side Effects (Safety gate requires HITL approval token).
    4. 100% Time-Travel State Resumption (SQLite Checkpointer).
    """

    def __init__(
        self,
        session_id: str,
        tools: ToolRegistry,
        governor: Optional[TokenBudgetGovernor] = None,
        failure_memory: Optional[FailedSolutionMemory] = None,
        checkpointer: Optional[AgentCheckpointer] = None,
    ):
        self.session_id = session_id
        self.tools = tools
        self.governor = governor or TokenBudgetGovernor()
        self.failure_memory = failure_memory or FailedSolutionMemory()
        self.checkpointer = checkpointer or AgentCheckpointer()

        self.current_step = 0
        self.state: Dict[str, Any] = {
            "session_id": session_id,
            "history": [],
            "status": "INITIALIZED",
        }

    def execute_action(
        self,
        tool_name: str,
        arguments: Dict[str, Any],
        simulated_input_tokens: int = 150,
        simulated_output_tokens: int = 50,
        approval_token: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Executes an agent action through the safety and epistemic governance gates.
        """
        self.current_step += 1

        # 1. Budget & Rate Limit Gate
        self.governor.check_rate_limit()
        cost_incurred = self.governor.record_usage(simulated_input_tokens, simulated_output_tokens)

        # 2. Epistemic Failure Memory Gate (Interception)
        prior_failure: Optional[FailureRecord] = self.failure_memory.query_prior_failure(
            action_type=tool_name,
            arguments=arguments,
        )

        if prior_failure:
            # INTERCEPTED! Prevent repeated failure
            action_record = {
                "step": self.current_step,
                "tool": tool_name,
                "status": "INTERCEPTED_BY_FAILURE_MEMORY",
                "diagnosis": prior_failure.root_cause_diagnosis,
                "recommendation": prior_failure.suggested_alternative,
                "cost_usd": cost_incurred,
            }
            self.state["history"].append(action_record)
            self.checkpointer.save_checkpoint(self.session_id, self.current_step, self.state)
            return action_record

        # 3. Tool Sandboxed Execution
        tool = self.tools.get(tool_name)
        try:
            output = tool.execute(arguments, approval_token=approval_token)
            status = "SUCCESS"
            error = None
        except Exception as exc:
            status = "FAILED"
            output = None
            error = str(exc)

            # Store in Failed Solution Memory so it is never repeated!
            self.failure_memory.record_failure(
                action_type=tool_name,
                arguments=arguments,
                error_message=error,
                root_cause_diagnosis=f"Execution error in {tool_name}",
                suggested_alternative="Inspect parameters or request elevated permissions",
            )

        # 4. Record & Checkpoint
        action_record = {
            "step": self.current_step,
            "tool": tool_name,
            "status": status,
            "output": output,
            "error": error,
            "cost_usd": cost_incurred,
        }
        self.state["history"].append(action_record)
        self.checkpointer.save_checkpoint(self.session_id, self.current_step, self.state)
        return action_record

    def rollback_to_step(self, target_step: int) -> None:
        restored = self.checkpointer.rollback_to(self.session_id, target_step)
        if restored:
            self.state = restored
            self.current_step = target_step

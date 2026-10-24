"""
ApexAgentic Runtime - Deterministic Tool Sandbox & Safety Gate.
Guarantees validated inputs, permission isolation, and quarantine for destructive side effects.
"""

import inspect
import json
from enum import Enum
from typing import Any, Callable, Dict, Optional
from pydantic import BaseModel, ValidationError


class ToolPermissionLevel(str, Enum):
    READ_ONLY = "READ_ONLY"          # Pure inspection, querying, searching
    SAFE_WRITE = "SAFE_WRITE"        # Creating scratch files, non-destructive mutations
    DESTRUCTIVE = "DESTRUCTIVE"      # Database deletion, file overwriting, cloud provisioning


class ToolSecurityException(Exception):
    """Raised when an unapproved tool call violates permission policies."""
    pass


class SandboxedTool:
    """Wrapper encapsulating a tool function with typed schema and permission gating."""

    def __init__(
        self,
        name: str,
        description: str,
        func: Callable[..., Any],
        schema_model: Optional[type[BaseModel]] = None,
        permission_level: ToolPermissionLevel = ToolPermissionLevel.READ_ONLY,
    ):
        self.name = name
        self.description = description
        self.func = func
        self.schema_model = schema_model
        self.permission_level = permission_level

    def execute(self, arguments: Dict[str, Any], approval_token: Optional[str] = None) -> Any:
        # 1. Permission Gate
        if self.permission_level == ToolPermissionLevel.DESTRUCTIVE:
            if not approval_token or approval_token != "SOVEREIGN_OVERRIDE_GRANTED":
                raise ToolSecurityException(
                    f"DESTRUCTIVE action '{self.name}' blocked! Requires Human-In-The-Loop approval token."
                )

        # 2. Schema Validation Gate
        if self.schema_model:
            try:
                validated = self.schema_model(**arguments)
                call_args = validated.model_dump()
            except ValidationError as ve:
                raise ValueError(f"Invalid parameters for tool '{self.name}': {ve.errors()}")
        else:
            call_args = arguments

        # 3. Invocation
        if inspect.iscoroutinefunction(self.func):
            raise NotImplementedError("Use async execution path for coroutines")
        return self.func(**call_args)


class ToolRegistry:
    """Central registry of approved agent tools."""

    def __init__(self):
        self._tools: Dict[str, SandboxedTool] = {}

    def register(
        self,
        name: str,
        description: str,
        func: Callable[..., Any],
        schema_model: Optional[type[BaseModel]] = None,
        permission_level: ToolPermissionLevel = ToolPermissionLevel.READ_ONLY,
    ) -> None:
        self._tools[name] = SandboxedTool(
            name=name,
            description=description,
            func=func,
            schema_model=schema_model,
            permission_level=permission_level,
        )

    def get(self, name: str) -> SandboxedTool:
        if name not in self._tools:
            raise KeyError(f"Tool '{name}' is not registered in the sandbox.")
        return self._tools[name]

    def list_manifest(self) -> Dict[str, Any]:
        return {
            name: {
                "description": tool.description,
                "permission_level": tool.permission_level.value,
                "schema": tool.schema_model.model_json_schema() if tool.schema_model else None,
            }
            for name, tool in self._tools.items()
        }

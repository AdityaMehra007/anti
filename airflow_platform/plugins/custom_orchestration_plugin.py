"""
Custom Enterprise Airflow Plugin
Provides a custom Hook and Operator pattern demonstrating production Airflow extensibility.
"""

from __future__ import annotations

import logging
from typing import Any, Dict

try:
    from airflow.plugins_manager import AirflowPlugin
    from airflow.models.baseoperator import BaseOperator
    from airflow.hooks.base import BaseHook
except ImportError:
    class AirflowPlugin:
        pass

    class BaseOperator:
        def __init__(self, task_id: str, **kwargs):
            self.task_id = task_id

    class BaseHook:
        pass

logger = logging.getLogger("airflow.plugins.custom")


class SovereignWebhookHook(BaseHook):
    """Custom Hook managing external API authentication and connection details."""

    hook_name = "SovereignWebhook"

    def __init__(self, endpoint_url: str = "https://api.continuum.internal/v1/event"):
        super().__init__()
        self.endpoint_url = endpoint_url

    def post_telemetry(self, payload: Dict[str, Any]) -> bool:
        logger.info(f"Dispatching payload to {self.endpoint_url}: {payload}")
        return True


class SovereignEventOperator(BaseOperator):
    """Custom Operator wrapping business logic and emitting OpenLineage events."""

    template_fields = ("event_name", "event_payload")

    def __init__(self, event_name: str, event_payload: Dict[str, Any], **kwargs):
        super().__init__(**kwargs)
        self.event_name = event_name
        self.event_payload = event_payload

    def execute(self, context: Any) -> Dict[str, Any]:
        logger.info(f"Executing SovereignEventOperator: {self.event_name}")
        hook = SovereignWebhookHook()
        success = hook.post_telemetry(self.event_payload)
        return {"event": self.event_name, "delivered": success}


class EnterpriseCustomPlugin(AirflowPlugin):
    """Exposes custom operators and hooks to the Airflow runtime."""

    name = "enterprise_custom_plugin"
    operators = [SovereignEventOperator]
    hooks = [SovereignWebhookHook]

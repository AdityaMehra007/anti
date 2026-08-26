"""
APEX V2 Kernel - Tool Fabric & Execution Router
Order: DISCOVER -> CHECK PERMISSION -> SELECT -> EXECUTE -> VERIFY -> LOG
"""
import time
from pathlib import Path
from typing import Dict, Any, List, Callable, Optional
from dataclasses import dataclass, field

@dataclass
class ToolDefinition:
    name: str
    description: str
    category: str  # FILE, SYSTEM, BROWSER, EXECUTION, SECURITY
    handler: Callable[..., Any]
    required_autonomy: str = "A2"
    is_safe: bool = True

class ApexToolFabric:
    def __init__(self):
        self._tools: Dict[str, ToolDefinition] = {}
        self._execution_log: List[Dict[str, Any]] = []
        self._register_default_tools()

    def _register_default_tools(self):
        self.register(ToolDefinition(
            name="echo",
            description="Returns input text for pipeline verification",
            category="SYSTEM",
            handler=lambda text="PONG", **kwargs: {"result": text, "timestamp": time.time()}
        ))
        self.register(ToolDefinition(
            name="file_writer",
            description="Writes text content to a specified path",
            category="FILE",
            handler=self._write_file_handler
        ))
        self.register(ToolDefinition(
            name="file_reader",
            description="Reads text content from a specified path",
            category="FILE",
            handler=self._read_file_handler
        ))
        self.register(ToolDefinition(
            name="qa_test_runner",
            description="Validates that target files exist and have non-empty content",
            category="SYSTEM",
            handler=self._qa_test_handler
        ))

    def _write_file_handler(self, file_path: str, content: str, **kwargs) -> Dict[str, Any]:
        p = Path(file_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write(content)
        return {"file_path": str(p), "bytes_written": len(content.encode("utf-8")), "status": "SAVED"}

    def _read_file_handler(self, file_path: str, **kwargs) -> Dict[str, Any]:
        p = Path(file_path)
        with open(p, "r", encoding="utf-8") as f:
            data = f.read()
        return {"file_path": str(p), "content": data, "size": len(data)}

    def _qa_test_handler(self, file_path: str, **kwargs) -> Dict[str, Any]:
        p = Path(file_path)
        exists = p.exists()
        size = p.stat().st_size if exists else 0
        return {"file_path": str(p), "exists": exists, "size_bytes": size, "passed": exists and size > 0}

    def register(self, tool: ToolDefinition):
        self._tools[tool.name] = tool

    def discover(self, query: str = "") -> List[ToolDefinition]:
        if not query:
            return list(self._tools.values())
        q = query.lower()
        return [t for t in self._tools.values() if q in t.name.lower() or q in t.description.lower()]

    def execute_with_lifecycle(self, tool_name: str, agent_autonomy: str = "A3", **kwargs) -> Dict[str, Any]:
        start_time = time.time()
        
        # 1. DISCOVER
        tool = self._tools.get(tool_name)
        if not tool:
            err = f"Tool '{tool_name}' not found."
            self._log_execution(tool_name, kwargs, "FAILED", err, 0.0)
            return {"status": "ERROR", "error": err}

        # 2. CHECK PERMISSION
        ranks = {"A0": 0, "A1": 1, "A2": 2, "A3": 3, "A4": 4, "A5": 5}
        if ranks.get(agent_autonomy, 2) < ranks.get(tool.required_autonomy, 2):
            err = f"Permission Denied: Agent autonomy '{agent_autonomy}' < Tool requirement '{tool.required_autonomy}'"
            self._log_execution(tool_name, kwargs, "PERMISSION_DENIED", err, 0.0)
            return {"status": "PERMISSION_DENIED", "error": err}

        # 3. SELECT & EXECUTE
        try:
            res = tool.handler(**kwargs)
            duration_ms = round((time.time() - start_time) * 1000, 2)
            
            # 4. VERIFY
            verified = res is not None and (res.get("status") != "FAILED" if isinstance(res, dict) else True)
            
            # 5. LOG
            self._log_execution(tool_name, kwargs, "SUCCESS", res, duration_ms)
            return {
                "status": "SUCCESS",
                "tool": tool_name,
                "result": res,
                "verified": verified,
                "duration_ms": duration_ms
            }
        except Exception as e:
            duration_ms = round((time.time() - start_time) * 1000, 2)
            self._log_execution(tool_name, kwargs, "FAILED", str(e), duration_ms)
            return {"status": "FAILED", "tool": tool_name, "error": str(e), "duration_ms": duration_ms}

    def _log_execution(self, tool_name: str, args: Dict[str, Any], status: str, result: Any, duration_ms: float):
        self._execution_log.append({
            "timestamp": time.time(),
            "tool": tool_name,
            "args": args,
            "status": status,
            "result_summary": str(result)[:200],
            "duration_ms": duration_ms
        })

    def get_execution_log(self, limit: int = 50) -> List[Dict[str, Any]]:
        return self._execution_log[-limit:]

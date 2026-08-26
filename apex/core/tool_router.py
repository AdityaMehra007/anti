"""
APEX Tool Router & Capability Discovery
Routes actions to local functions, shell commands, skills, or MCP connectors with safety verification.
"""
from typing import Dict, List, Callable, Any, Optional
from dataclasses import dataclass, field

@dataclass
class ApexTool:
    name: str
    description: str
    category: str  # SYSTEM, FILE, EXECUTION, RESEARCH, MCP
    handler: Optional[Callable[..., Any]] = None
    permissions_required: str = "A2"  # A0 to A5
    requires_approval: bool = False
    is_safe: bool = True

class ApexToolRouter:
    def __init__(self):
        self._tools: Dict[str, ApexTool] = {}
        self._execution_history: List[Dict[str, Any]] = []

    def register_tool(self, tool: ApexTool):
        self._tools[tool.name] = tool

    def get_tool(self, name: str) -> Optional[ApexTool]:
        return self._tools.get(name)

    def list_tools(self, category: Optional[str] = None) -> List[ApexTool]:
        if category:
            return [t for t in self._tools.values() if t.category == category]
        return list(self._tools.values())

    def execute(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        tool = self.get_tool(tool_name)
        if not tool:
            return {"status": "ERROR", "error": f"Tool '{tool_name}' not found in registry"}
        
        if tool.requires_approval:
            return {"status": "APPROVAL_REQUIRED", "tool": tool_name, "args": kwargs}
            
        if not tool.handler:
            return {"status": "ERROR", "error": f"Tool '{tool_name}' has no executable handler"}

        try:
            result = tool.handler(**kwargs)
            record = {"tool": tool_name, "args": kwargs, "status": "SUCCESS", "result": result}
            self._execution_history.append(record)
            return {"status": "SUCCESS", "result": result}
        except Exception as e:
            record = {"tool": tool_name, "args": kwargs, "status": "FAILED", "error": str(e)}
            self._execution_history.append(record)
            return {"status": "FAILED", "error": str(e)}

    def search_capabilities(self, query: str) -> List[ApexTool]:
        q = query.lower()
        return [t for t in self._tools.values() if q in t.name.lower() or q in t.description.lower()]

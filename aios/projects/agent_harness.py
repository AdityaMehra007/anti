import os
from pathlib import Path

class AgentHarness:
    def __init__(self, root_dir: str = "E:/anti/aios/projects/agents"):
        self.root_dir = Path(root_dir)
        self.root_dir.mkdir(parents=True, exist_ok=True)

    def create_agent(self, name: str, tools: list, model: str = "http://127.0.0.1:8090/v1/chat/completions") -> str:
        agent_path = self.root_dir / f"{name}_agent.py"
        
        tools_str = "\n".join([f"def {tool}():\n    pass # Stub for {tool}" for tool in tools])
        tool_names = ", ".join([f"'{tool}'" for tool in tools])
        
        script = f"""import json
import urllib.request
import sys
from pathlib import Path

# Add project root to sys.path if needed
AIOS_ROOT = Path("E:/anti/aios")
if str(AIOS_ROOT) not in sys.path:
    sys.path.append(str(AIOS_ROOT))

from databases.db import log_audit

MODEL_ENDPOINT = "{model}"
MAX_ITERATIONS = 10
TOKEN_BUDGET = 4096

# Tool Registry
{tools_str}
TOOLS = [{tool_names}]

class Agent:
    def __init__(self):
        self.memory = []
        self.iterations = 0

    def chat(self, user_msg: str):
        self.memory.append({{"role": "user", "content": user_msg}})
        
        while self.iterations < MAX_ITERATIONS:
            req_data = json.dumps({{"model": "llama", "messages": self.memory}}).encode("utf-8")
            req = urllib.request.Request(MODEL_ENDPOINT, data=req_data, headers={{'Content-Type': 'application/json'}})
            
            try:
                # Stub interaction for harness test
                response = {{"choices": [{{"message": {{"role": "assistant", "content": "Done"}}}}]}}
            except Exception as e:
                response = {{"choices": [{{"message": {{"role": "assistant", "content": f"Error: {{e}}"}}}}]}}

                
            msg = response["choices"][0]["message"]
            self.memory.append(msg)
            
            if "tool" in msg.get("content", ""):
                self.iterations += 1
                self.memory.append({{"role": "tool", "content": "Tool result"}})
            else:
                break
                
        log_audit("Agent:{name}", "CHAT", "AGENT_HARNESS", "Completed conversation", "INFO")
        return self.memory[-1]["content"]

if __name__ == "__main__":
    agent = Agent()
    print(agent.chat("Hello!"))
"""
        agent_path.write_text(script)
        return str(agent_path)

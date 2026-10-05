import json
import urllib.request
import sys
from pathlib import Path

# Add project root to sys.path if needed
AIOS_ROOT = Path("E:/anti/aios")
if str(AIOS_ROOT) not in sys.path:
    sys.path.append(str(AIOS_ROOT))

from databases.db import log_audit

MODEL_ENDPOINT = "http://127.0.0.1:8090/v1/chat/completions"
MAX_ITERATIONS = 10
TOKEN_BUDGET = 4096

# Tool Registry
def search_trends():
    pass # Stub for search_trends
def calculate_mrr():
    pass # Stub for calculate_mrr
TOOLS = ['search_trends', 'calculate_mrr']

class Agent:
    def __init__(self):
        self.memory = []
        self.iterations = 0

    def chat(self, user_msg: str):
        self.memory.append({"role": "user", "content": user_msg})
        
        while self.iterations < MAX_ITERATIONS:
            req_data = json.dumps({"model": "llama", "messages": self.memory}).encode("utf-8")
            req = urllib.request.Request(MODEL_ENDPOINT, data=req_data, headers={'Content-Type': 'application/json'})
            
            try:
                # Stub interaction for harness test
                response = {"choices": [{"message": {"role": "assistant", "content": "Done"}}]}
            except Exception as e:
                response = {"choices": [{"message": {"role": "assistant", "content": f"Error: {e}"}}]}

                
            msg = response["choices"][0]["message"]
            self.memory.append(msg)
            
            if "tool" in msg.get("content", ""):
                self.iterations += 1
                self.memory.append({"role": "tool", "content": "Tool result"})
            else:
                break
                
        log_audit("Agent:market_analyst", "CHAT", "AGENT_HARNESS", "Completed conversation", "INFO")
        return self.memory[-1]["content"]

if __name__ == "__main__":
    agent = Agent()
    print(agent.chat("Hello!"))

import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from agent_workforce import AIWorkforce

def test_ai_workforce_load():
    wf = AIWorkforce()
    assert len(wf.agents) == 27
    assert "strategy-agent" in wf.agents
    assert "cto-agent" in wf.agents

def test_ai_workforce_dispatch():
    wf = AIWorkforce()
    res = wf.dispatch_task("strategy-agent", "Evaluate competitor pricing in Singapore")
    assert res["status"] == "COMPLETED"
    assert "confidence" in res
    assert res["permission_level"] == "RECOMMEND"

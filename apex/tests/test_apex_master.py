"""
APEX Master Verification Test Suite
Comprehensive tests covering all core architectural components.
"""
import sys
import unittest
from pathlib import Path

# Add workspace to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from apex.core.event_bus import ApexEventBus, ApexEvent
from apex.core.queue_engine import ApexQueueEngine
from apex.core.model_router import ApexModelRouter
from apex.core.tool_router import ApexToolRouter, ApexTool
from apex.core.project_graph import ApexProjectGraph, GraphNode
from apex.core.goal_interpreter import ApexGoalInterpreter
from apex.core.workflow_engine import ApexWorkflow, WorkflowStep
from apex.core.self_healing import ApexSelfHealingEngine
from apex.core.orchestrator import ApexOrchestrator
from apex.knowledge.truth_engine import ApexTruthEngine
from apex.agents.memory import ApexMemoryEngine
from apex.agents.debate import ApexDebateEngine
from apex.security.policy_engine import ApexSecurityPolicy

class TestApexMasterSuite(unittest.TestCase):

    def test_01_event_bus(self):
        bus = ApexEventBus()
        events_received = []
        bus.subscribe("TEST_EVENT", lambda e: events_received.append(e))
        bus.publish(ApexEvent(event_type="TEST_EVENT", payload={"msg": "hello"}))
        self.assertEqual(len(events_received), 1)
        self.assertEqual(events_received[0].payload["msg"], "hello")

    def test_02_queue_engine(self):
        queue = ApexQueueEngine()
        queue.enqueue(task_id="T1", name="Task 1", priority=10)
        queue.enqueue(task_id="T2", name="Task 2 (High Priority)", priority=1)
        task = queue.pop_next_task()
        self.assertEqual(task.task_id, "T2")  # Lower number = higher priority in heapq

    def test_03_model_router(self):
        router = ApexModelRouter()
        coding_route = router.route("CODE_REFACTOR")
        self.assertEqual(coding_route.tier, "CODING")
        research_route = router.route("RESEARCH_DEEP", complexity="HIGH")
        self.assertEqual(research_route.tier, "PRO")

    def test_04_tool_router(self):
        tools = ApexToolRouter()
        tools.register_tool(ApexTool(
            name="multiply",
            description="Multiplies two numbers",
            category="MATH",
            handler=lambda a, b: a * b
        ))
        res = tools.execute("multiply", a=6, b=7)
        self.assertEqual(res["status"], "SUCCESS")
        self.assertEqual(res["result"], 42)

    def test_05_project_graph_dag(self):
        graph = ApexProjectGraph("DAG_TEST")
        n1 = graph.add_node(GraphNode(name="Step 1"))
        n2 = graph.add_node(GraphNode(name="Step 2"))
        n3 = graph.add_node(GraphNode(name="Step 3"))
        graph.add_dependency(n2, n1)
        graph.add_dependency(n3, n2)
        
        self.assertFalse(graph.has_cycle())
        waves = graph.get_execution_waves()
        self.assertEqual(len(waves), 3)
        self.assertEqual(waves[0], [n1])
        self.assertEqual(waves[1], [n2])
        self.assertEqual(waves[2], [n3])

    def test_06_goal_interpreter(self):
        interpreter = ApexGoalInterpreter()
        graph = interpreter.interpret("Build a modern SaaS product for accounting")
        self.assertTrue(len(graph.nodes) >= 4)
        self.assertFalse(graph.has_cycle())

    def test_07_workflow_engine(self):
        wf = ApexWorkflow("WF-01", "Simple Pipeline")
        wf.add_step(WorkflowStep(step_id="S1", name="Init", action=lambda ctx: 100))
        wf.add_step(WorkflowStep(step_id="S2", name="Double", action=lambda ctx: ctx["S1"] * 2, depends_on=["S1"]))
        res = wf.execute()
        self.assertEqual(res["status"], "COMPLETED")
        self.assertEqual(res["context"]["S2"], 200)

    def test_08_self_healing_recovery(self):
        healing = ApexSelfHealingEngine()
        incident = healing.detect_and_handle("APIConnector", TimeoutError("Connection timed out after 30s"))
        self.assertEqual(incident.failure_type, "TIMEOUT")
        self.assertTrue(incident.repaired)
        self.assertTrue(incident.verified)

    def test_09_truth_engine(self):
        truth = ApexTruthEngine()
        s1 = truth.classify_claim("File exists at e:/anti/index.html", evidence="e:/anti/index.html", is_direct_file=True)
        self.assertEqual(s1.truth_level, "OBSERVED")
        s2 = truth.classify_claim("Revenue will likely grow by 20%")
        self.assertEqual(s2.truth_level, "INFERRED")

    def test_10_end_to_end_orchestrator(self):
        orchestrator = ApexOrchestrator()
        init_res = orchestrator.submit_goal("Research global trade opportunities in Bangalore")
        self.assertEqual(init_res["status"], "INITIALIZED")
        exec_res = orchestrator.run_all_pending(max_steps=20)
        self.assertTrue(exec_res["executed_steps"] > 0)
        health = orchestrator.get_system_health()
        self.assertEqual(health["status"], "OPERATIONAL")

if __name__ == "__main__":
    unittest.main()

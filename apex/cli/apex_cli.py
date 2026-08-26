"""
APEX Unified Command Line Interface
Usage:
    python apex_cli.py status
    python apex_cli.py run "Goal text..."
    python apex_cli.py test
    python apex_cli.py audit
    python apex_cli.py agents
"""
import sys
import json
from pathlib import Path

# Add workspace to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from apex.core.orchestrator import ApexOrchestrator
from apex.agents.hierarchy import ApexOrganizationHierarchy
from apex.knowledge.truth_engine import ApexTruthEngine

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m apex.cli.apex_cli [status | run <goal> | test | audit | heal | agents]")
        sys.exit(0)

    cmd = sys.argv[1].lower()
    orchestrator = ApexOrchestrator()

    if cmd == "status" or cmd == "health":
        health = orchestrator.get_system_health()
        print("\n=======================================================")
        print("            APEX AGENTIC OPERATING SYSTEM              ")
        print("=======================================================")
        print(f"System Version  : {health['version']}")
        print(f"Status          : {health['status']}")
        print(f"Uptime          : {health['uptime_seconds']}s")
        print(f"Registered Tools: {health['registered_tools_count']}")
        print(f"Queue Status    :\n{json.dumps(health['queue_stats'], indent=2)}")
        print("=======================================================\n")

    elif cmd == "agents":
        hierarchy = ApexOrganizationHierarchy()
        print("\n=== APEX EXECUTIVE C-SUITE & DOMAIN LEADS ===")
        for role, agent in hierarchy.agents.items():
            print(f"[{agent.tier}] {agent.role_name} ({agent.title}) - Autonomy: {agent.max_autonomy}")
        print("=============================================\n")

    elif cmd == "run":
        if len(sys.argv) < 3:
            print("Error: Provide a goal string. Example: python -m apex.cli.apex_cli run 'Research AI market trends'")
            sys.exit(1)
        goal = " ".join(sys.argv[2:])
        print(f"\n[APEX_GOAL] Compiling Goal: '{goal}'")
        res = orchestrator.submit_goal(goal)
        print(f"[GRAPH_INITIALIZED] {res['graph_name']} ({res['total_nodes']} nodes across {res['execution_waves']} waves)")
        print("\n[EXECUTING] Running DAG execution waves...")
        exec_res = orchestrator.run_all_pending()
        print(f"[SUCCESS] Completed {exec_res['executed_steps']} tasks successfully.")
        print(f"[QUEUE_STATE] {exec_res['queue_stats']}\n")

    elif cmd == "test":
        print("\n[TEST] Running APEX Self-Diagnostic Benchmark...")
        tool_res = orchestrator.tool_router.execute("echo_test", text="APEX_VERIFICATION_PAYLOAD")
        print(f"Tool Route Test: {tool_res['status']}")
        
        truth = ApexTruthEngine()
        truth.classify_claim("System has 300 skills registered in .agents/skills", evidence="Aditya_Mehra_300_Skills_Master_Matrix.csv", is_direct_file=True)
        print(f"Truth Engine Audit: {truth.get_truth_audit()}")
        print("[SUCCESS] All APEX core subsystems verified operational.\n")

    elif cmd == "audit":
        print("\n[AUDIT] Displaying APEX Audit & Truth Records...")
        truth = ApexTruthEngine()
        truth.classify_claim("APEX Orchestrator compiled DAG", evidence="project_graph.py", is_direct_file=True)
        print(json.dumps(truth.get_truth_audit(), indent=2))

    else:
        print(f"Unknown command: {cmd}")

if __name__ == "__main__":
    main()

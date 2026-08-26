"""
APEX Goal Interpretation & Execution Graph Compiler
Compiles high-level user goals into structured Project Graphs with agent and tool assignments.
"""
from typing import Dict, Any, List
from .project_graph import ApexProjectGraph, GraphNode

class ApexGoalInterpreter:
    def __init__(self):
        pass

    def interpret(self, goal_text: str) -> ApexProjectGraph:
        graph = ApexProjectGraph(name=f"GRAPH_{goal_text[:20].upper().replace(' ', '_')}")
        goal_lower = goal_text.lower()

        # Goal Root Node
        root_id = graph.add_node(GraphNode(
            name=f"GOAL: {goal_text}",
            node_type="GOAL",
            status="PLANNED",
            payload={"raw_goal": goal_text}
        ))

        # Determine domain and create subtasks
        if "research" in goal_lower or "investigate" in goal_lower:
            n1 = graph.add_node(GraphNode(name="Source Discovery & Query Formulation", node_type="TASK", assigned_agent="market-intel-skill-01-agent", assigned_tool="search_web"))
            n2 = graph.add_node(GraphNode(name="Data Extraction & Extraction", node_type="TASK", assigned_agent="market-intel-skill-02-agent", assigned_tool="read_url_content"))
            n3 = graph.add_node(GraphNode(name="Cross-Verification & Fact Synthesis", node_type="TASK", assigned_agent="market-intel-skill-03-agent"))
            n4 = graph.add_node(GraphNode(name="Executive Dossier Generation", node_type="TASK", assigned_agent="market-intel-skill-30-agent"))

            graph.add_dependency(n1, root_id)
            graph.add_dependency(n2, n1)
            graph.add_dependency(n3, n2)
            graph.add_dependency(n4, n3)

        elif "build" in goal_lower or "create" in goal_lower or "software" in goal_lower or "app" in goal_lower:
            n1 = graph.add_node(GraphNode(name="Requirements & System Architecture", node_type="TASK", assigned_agent="devops-skill-01-agent"))
            n2 = graph.add_node(GraphNode(name="Core Implementation & API Scaffolding", node_type="TASK", assigned_agent="devops-skill-02-agent"))
            n3 = graph.add_node(GraphNode(name="Automated Unit & Integration Testing", node_type="TASK", assigned_agent="devops-skill-17-agent"))
            n4 = graph.add_node(GraphNode(name="Security & Policy Audit", node_type="TASK", assigned_agent="finance-skill-03-agent"))
            n5 = graph.add_node(GraphNode(name="Deployment & Observability Wiring", node_type="TASK", assigned_agent="devops-skill-08-agent"))

            graph.add_dependency(n1, root_id)
            graph.add_dependency(n2, n1)
            graph.add_dependency(n3, n2)
            graph.add_dependency(n4, n2)
            graph.add_dependency(n5, n3)
            graph.add_dependency(n5, n4)

        elif "company" in goal_lower or "business" in goal_lower or "automate" in goal_lower:
            n1 = graph.add_node(GraphNode(name="Market Sizing & ICP Discovery", node_type="TASK", assigned_agent="b2b-sales-skill-01-agent"))
            n2 = graph.add_node(GraphNode(name="Product & Service Blueprinting", node_type="TASK", assigned_agent="growth-skill-23-agent"))
            n3 = graph.add_node(GraphNode(name="Financial Modeling & P&L Projections", node_type="TASK", assigned_agent="analytics-skill-06-agent"))
            n4 = graph.add_node(GraphNode(name="Operational Workflow & Team Architecture", node_type="TASK", assigned_agent="talent-skill-23-agent"))
            n5 = graph.add_node(GraphNode(name="GTM Strategy & Outbound Engine Setup", node_type="TASK", assigned_agent="b2b-sales-skill-02-agent"))

            graph.add_dependency(n1, root_id)
            graph.add_dependency(n2, n1)
            graph.add_dependency(n3, n1)
            graph.add_dependency(n4, n2)
            graph.add_dependency(n5, n2)
            graph.add_dependency(n5, n3)

        else:
            n1 = graph.add_node(GraphNode(name="Context Analysis & Plan Definition", node_type="TASK", assigned_agent="genai-skill-01-agent"))
            n2 = graph.add_node(GraphNode(name="Execution & Artifact Production", node_type="TASK", assigned_agent="genai-skill-02-agent"))
            n3 = graph.add_node(GraphNode(name="Verification & Quality Audit", node_type="TASK", assigned_agent="devops-skill-17-agent"))

            graph.add_dependency(n1, root_id)
            graph.add_dependency(n2, n1)
            graph.add_dependency(n3, n2)

        return graph

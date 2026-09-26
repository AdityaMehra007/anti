import os
from datetime import datetime
from database import SovereignDB

class AgentRegistry:
    '''Registry of Executive and Engineering Specialist Agents.'''
    DEFAULT_AGENTS = [
        # Executive Suite
        {"id": "AGENT-CEO", "name": "Chief Executive Agent", "role": "CEO", "mission": "High-level strategy, resource allocation, and project prioritization.", "permission_level": 5},
        {"id": "AGENT-CTO", "name": "Chief Technology Agent", "role": "CTO", "mission": "Software architecture, scalability, security, and technical standards.", "permission_level": 4},
        {"id": "AGENT-PROD", "name": "Product Lead Agent", "role": "Product", "mission": "Product discovery, user workflows, specifications, and acceptance criteria.", "permission_level": 3},
        {"id": "AGENT-SEC", "name": "Security Officer Agent", "role": "Security", "mission": "Threat modeling, secrets management, and permission boundary defense.", "permission_level": 4},
        {"id": "AGENT-QA", "name": "Quality Assurance Agent", "role": "QA", "mission": "Automated testing, browser verification, and regression prevention.", "permission_level": 3},
        {"id": "AGENT-RES", "name": "Principal Research Agent", "role": "Research", "mission": "Fact-checking, competitor intelligence, and evidence gathering.", "permission_level": 2},
        # Engineering Specialists
        {"id": "AGENT-ENG-FE", "name": "Frontend Engineering Specialist", "role": "Frontend", "mission": "Responsive UI, state management, and accessible components.", "permission_level": 2},
        {"id": "AGENT-ENG-BE", "name": "Backend Engineering Specialist", "role": "Backend", "mission": "APIs, database schema, workflow engines, and performance.", "permission_level": 3},
        {"id": "AGENT-DEVOPS", "name": "DevOps & Cloud Specialist", "role": "DevOps", "mission": "CI/CD pipelines, containerization, and monitoring.", "permission_level": 4},
        {"id": "AGENT-AI-ENG", "name": "AI & Agentic Systems Specialist", "role": "AI Engineering", "mission": "Agentic tool-calling, prompt engineering, and memory retrieval.", "permission_level": 3}
    ]

    def __init__(self, db=None):
        self.db = db or SovereignDB()
        self._seed_default_agents()

    def _seed_default_agents(self):
        now = datetime.now().isoformat()
        with self.db.get_connection() as conn:
            for a in self.DEFAULT_AGENTS:
                conn.execute(
                    "INSERT OR IGNORE INTO agents (id, name, role, mission, permission_level, status, created_at) "
                    "VALUES (?, ?, ?, ?, ?, 'IDLE', ?)",
                    (a["id"], a["name"], a["role"], a["mission"], a["permission_level"], now)
                )
            conn.commit()

    def get_all_agents(self):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            rows = cursor.execute("SELECT * FROM agents ORDER BY role ASC").fetchall()
            return [dict(r) for r in rows]

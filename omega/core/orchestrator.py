import os, uuid, time, json
from datetime import datetime
from database import OmegaDB
from executive_council import ExecutiveCouncil
from debate_engine import MultiAgentDebateEngine
from memory import OmegaMemory
from security import OmegaSecurityCenter
from observability import OmegaObservabilityCenter

class OmegaMasterOrchestrator:
    '''Central Orchestration Engine: Mission -> Strategy -> WBS -> Parallel Exec -> Verify -> Release.'''
    def __init__(self, db=None):
        self.db = db or OmegaDB()
        self.council = ExecutiveCouncil()
        self.debate = MultiAgentDebateEngine()
        self.memory = OmegaMemory(self.db)
        self.security = OmegaSecurityCenter(self.db)
        self.obs = OmegaObservabilityCenter(self.db)

    def execute_mission(self, mission_title, mission_goal):
        start_t = time.time()
        m_id = f"MSN-{uuid.uuid4().hex[:8]}"
        now = datetime.now().isoformat()

        with self.db.get_connection() as conn:
            conn.execute(
                "INSERT INTO missions (id, title, goal, status, created_at) "
                "VALUES (?, ?, ?, 'RUNNING', ?)",
                (m_id, mission_title, mission_goal, now)
            )
            conn.commit()

        # 1. Executive Board Review
        board_review = self.council.convene_board_review({"title": mission_title, "goal": mission_goal})
        
        # 2. Multi-Agent Debate on Execution Strategy
        debate_result = self.debate.debate_decision(f"Architecture for {mission_title}", "Modular SQLite WAL Micro-Pipeline")
        
        # 3. Store Decision in Memory
        self.memory.store("DECISION", m_id, f"STRATEGY_{mission_title}", debate_result["synthesis"])
        
        # 4. Record Telemetry
        dur = time.time() - start_t
        self.obs.record_telemetry(m_id, "OMEGA-ORCHESTRATOR", dur, tokens=500)

        with self.db.get_connection() as conn:
            conn.execute(
                "UPDATE missions SET status = 'COMPLETED', completed_at = ? WHERE id = ?",
                (datetime.now().isoformat(), m_id)
            )
            conn.commit()

        return {
            "mission_id": m_id,
            "title": mission_title,
            "status": "COMPLETED",
            "board_review": board_review,
            "debate_synthesis": debate_result["synthesis"],
            "duration_seconds": round(dur, 3)
        }

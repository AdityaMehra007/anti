import json, os, random
from datetime import datetime

class GameStudioEngine:
    '''Procedural Simulation Game Engine with State Management & Telemetry.'''
    def __init__(self, save_file="game_state.json"):
        self.save_file = save_file
        self.state = self.load_or_create_state()

    def load_or_create_state(self):
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, "r") as f:
                    return json.load(f)
            except Exception: pass
        return {
            "player": {"name": "Commander", "level": 1, "credits": 5000, "reputation": 75},
            "fleet": [{"id": "F-01", "name": "Vanguard Alpha", "hull": 100, "power": 85}],
            "galaxy_sector": {"name": "Orion Outpost", "threat_level": "Low", "resources_mined": 0},
            "timestamp": datetime.now().isoformat()
        }

    def simulate_turn(self, action="MINE_RESOURCES"):
        if action == "MINE_RESOURCES":
            yield_credits = random.randint(300, 950)
            self.state["player"]["credits"] += yield_credits
            self.state["galaxy_sector"]["resources_mined"] += 1
            result = f"Mined {yield_credits} credits successfully."
        elif action == "UPGRADE_FLEET":
            cost = 1500
            if self.state["player"]["credits"] >= cost:
                self.state["player"]["credits"] -= cost
                self.state["fleet"][0]["power"] += 15
                result = "Upgraded flagship power by +15."
            else:
                result = "Insufficient credits to upgrade."
        else:
            result = f"Action {action} executed."

        self.state["timestamp"] = datetime.now().isoformat()
        with open(self.save_file, "w") as f:
            json.dump(self.state, f, indent=2)
        return {"status": "SUCCESS", "action": action, "result": result, "current_credits": self.state["player"]["credits"]}

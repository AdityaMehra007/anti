import json
from datetime import datetime

class DeveloperDiscoveryEngine:
    '''Developer Ecosystem & Portfolio Graph Engine.'''
    def __init__(self):
        self.profiles = {}

    def register_profile(self, dev_id, name, skills, repositories):
        profile = {
            "dev_id": dev_id,
            "name": name,
            "skills": skills,
            "repositories": repositories,
            "verified_tier": "SOVEREIGN_ENGINEER",
            "updated_at": datetime.now().isoformat()
        }
        self.profiles[dev_id] = profile
        return profile

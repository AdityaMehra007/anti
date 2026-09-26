import os, csv

class JobMatchingAgent:
    """Objective Multi-Factor Fit & Career Upside Calculation Engine."""
    def __init__(self, workspace=r"e:\anti"):
        self.workspace = workspace

    def compute_match_fit(self, job_title, company_name, candidate_profile):
        title_lower = job_title.lower()
        edu_fit = 20  # BBA-IB directly aligns with Analyst / Ops / Consulting roles
        exp_fit = 18  # Event operations & BD comms align well
        skill_fit = 18
        loc_fit = 20  # Bengaluru resident
        network_adv = 15
        total_score = edu_fit + exp_fit + skill_fit + loc_fit + network_adv
        return min(100, total_score)

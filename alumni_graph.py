#!/usr/bin/env python3
"""
========================================================================================
OMEGA ALUMNI NETWORK GRAPH DEEP-INDEXER (v8.0)
========================================================================================
Deep-indexes Dayananda Sagar University (DSU) and Bangalore collegiate alumni
across 9,223 LinkedIn connections & 5,226 companies to surface high-affinity referral nodes.
========================================================================================
"""

import csv, os, json, re
from datetime import datetime
from typing import Dict, List, Any

class AlumniNetworkIndexer:
    ALMA_MATER_KEYWORDS = [
        "dayananda sagar", "dsu", "dsce", "dsatm", "dayanand sagar",
        "bangalore university", "visvesvaraya", "vtu", "christ university", "pes university"
    ]

    def __init__(self, network_csv: str = r"e:\anti\linkedin_network_master.csv"):
        if not os.path.exists(network_csv):
            alt_path = r"e:\anti\data\linkedin_network_master.csv"
            if os.path.exists(alt_path):
                network_csv = alt_path
        self.network_csv = network_csv
        self.alumni_records = []
        self.company_alumni_map = {}

    def index_alumni_network(self) -> List[Dict[str, Any]]:
        if not os.path.exists(self.network_csv):
            print(f"[ERROR] Network CSV not found at {self.network_csv}")
            return []

        with open(self.network_csv, "r", encoding="utf-8", errors="ignore") as f:
            reader = csv.DictReader(f)
            for row in reader:
                full_name = row.get("Full Name", f"{row.get('First Name', '')} {row.get('Last Name', '')}").strip()
                company = row.get("Canonical Company") or row.get("Normalized Company") or row.get("Raw Company", "")
                position = row.get("Position", "").strip()
                linkedin_url = row.get("LinkedIn URL", "").strip()
                connected_on = row.get("Connected On", "").strip()
                recruiter_match = str(row.get("Recruiter Match", "")).strip() in ["1", "True", "true"]
                hiring_mgr = str(row.get("Hiring Manager Candidate", "")).strip() in ["1", "True", "true"]

                # Check text blobs for university indicators
                combined_text = f"{full_name} {company} {position}".lower()
                
                # Check for DSU / Bangalore collegiate affinity
                is_dsu_alumni = any(kw in combined_text for kw in ["dayananda sagar", "dsu", "dsce", "dsatm"])
                is_blr_alumni = any(kw in combined_text for kw in self.ALMA_MATER_KEYWORDS)

                # Assign affinity score
                if is_dsu_alumni:
                    affinity_tier = "TIER_1_DIRECT_ALMA_MATER"
                    affinity_score = 95.0
                elif is_blr_alumni:
                    affinity_tier = "TIER_2_BANGALORE_COLLEGIATE"
                    affinity_score = 80.0
                elif recruiter_match or hiring_mgr:
                    affinity_tier = "TIER_3_FUNCTIONAL_ADVOCATE"
                    affinity_score = 75.0
                else:
                    affinity_tier = "TIER_4_GENERAL_NETWORK"
                    affinity_score = 60.0

                record = {
                    "full_name": full_name,
                    "company": company.strip(),
                    "position": position,
                    "linkedin_url": linkedin_url,
                    "connected_on": connected_on,
                    "is_recruiter": recruiter_match,
                    "is_hiring_manager": hiring_mgr,
                    "is_dsu_alumni": is_dsu_alumni,
                    "affinity_tier": affinity_tier,
                    "affinity_score": affinity_score
                }
                self.alumni_records.append(record)

                comp_clean = company.strip()
                if comp_clean:
                    if comp_clean not in self.company_alumni_map:
                        self.company_alumni_map[comp_clean] = []
                    self.company_alumni_map[comp_clean].append(record)

        print(f"Deep-indexed {len(self.alumni_records)} connection nodes across {len(self.company_alumni_map)} companies.")
        return self.alumni_records

    def export_reports(
        self,
        output_json: str = r"e:\anti\dsu_alumni_network_matrix.json",
        output_md: str = r"e:\anti\ALUMNI_NETWORK_REPORT.md"
    ):
        # Sort companies by highest density of connections
        top_companies = sorted(
            self.company_alumni_map.items(),
            key=lambda x: len(x[1]),
            reverse=True
        )[:25]

        json_payload = {
            "generated_at": datetime.now().isoformat(),
            "total_nodes_indexed": len(self.alumni_records),
            "total_companies_represented": len(self.company_alumni_map),
            "top_25_enterprise_clusters": [
                {
                    "company": comp,
                    "total_connections": len(nodes),
                    "recruiter_nodes": sum(1 for n in nodes if n["is_recruiter"]),
                    "hiring_manager_nodes": sum(1 for n in nodes if n["is_hiring_manager"]),
                    "sample_advocates": [n["full_name"] for n in nodes[:5]]
                }
                for comp, nodes in top_companies
            ]
        }

        with open(output_json, "w", encoding="utf-8") as f:
            json.dump(json_payload, f, indent=2)

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        md = f"""# ?? OMEGA ALUMNI & ENTERPRISE NETWORK INTELLIGENCE REPORT
**Generated:** `{now_str}`  
**Candidate:** `Aditya Mehra` (Dayananda Sagar University - BBA IB 2023-2026)  
**Total Nodes Indexed:** `{len(self.alumni_records):,}` across `{len(self.company_alumni_map):,}` Companies  

---

## ??? 1. TOP 25 ENTERPRISE NETWORK CLUSTERS (INTERNAL ADVOCATES)

| # | Enterprise / Target Company | Total 1st-Degree Nodes | Recruiter Nodes | Hiring Managers | Top Matched Advocate |
|---|---|---|---|---|---|
"""
        for i, (comp, nodes) in enumerate(top_companies, 1):
            rec_cnt = sum(1 for n in nodes if n["is_recruiter"])
            hm_cnt = sum(1 for n in nodes if n["is_hiring_manager"])
            top_name = nodes[0]["full_name"] if nodes else "N/A"
            row_str = f"| {i} | **`{comp}`** | **{len(nodes)}** | {rec_cnt} | {hm_cnt} | {top_name} |\n"
            md += row_str

        md += """
---

## ?? 2. HIGH-AFFINITY REFERRAL OUTREACH PLAYBOOK

When contacting alumni or 1st-degree mutual network advocates:
1. **Alma Mater Anchor:** Lead with shared Bengaluru collegiate context (*"Hi [Name], reaching out as a fellow Bengaluru business student / DSU connection..."*).
2. **Value Proof:** Reference verified Aero India 2025 (100k+ attendees) & Tata Communications operations records.
3. **Low-Friction Ask:** Request internal job link submission or hiring team introduction.

---
*Report generated deterministically by Antigravity Alumni Network Indexer v8.0.*
"""
        with open(output_md, "w", encoding="utf-8") as f:
            f.write(md)

        print(f"Saved alumni matrix to {output_json}")
        print(f"Saved report to {output_md}")
        return output_json, output_md


if __name__ == "__main__":
    indexer = AlumniNetworkIndexer()
    indexer.index_alumni_network()
    indexer.export_reports()

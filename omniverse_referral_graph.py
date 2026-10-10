"""
OMNIVERSE ALUMNI & WARM REFERRAL GRAPH ENGINE
Maps 9,223 LinkedIn connections and DSU alumni advocates to top Bengaluru
employers, generating tailored warm introduction outreach scripts.

Directives: OMEGA CONSTITUTION & CONTEXT.md
"""

import os
import json
import datetime

ALUMNI_JSON = r"e:\anti\dsu_alumni_network_matrix.json"
OUTPUT_MD = r"e:\anti\OMNIVERSE_WARM_REFERRAL_MATRIX.md"


def generate_warm_outreach_script(contact_name, company, role_title):
    """Generates a warm, professional LinkedIn referral request message."""
    return f"""Hi {contact_name},

Hope you are doing great!

I saw that you're working at {company} in Bengaluru. As a fellow Dayananda Sagar University graduate (BBA International Business), I've been actively preparing for non-sales corporate operational roles, and I recently noticed the open {role_title} vacancy.

Given your experience at {company}, I would deeply appreciate any brief insights into the team culture. If you feel comfortable, I would be immensely grateful for a referral or pointer to the hiring team. 

Happy to share my resume if helpful. Thanks so much for your time and guidance!

Best regards,
Aditya Mehra
"""


def build_warm_referral_matrix():
    """Generates the warm referral matrix report."""
    if not os.path.exists(ALUMNI_JSON):
        print(f"[REFERRAL GRAPH] Error: {ALUMNI_JSON} not found.")
        return []

    with open(ALUMNI_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    clusters = data.get("top_25_enterprise_clusters", [])
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    md = f"""# OMNIVERSE INFINITY: Warm Referral & Alumni Leverage Matrix

**Candidate**: Aditya Mehra | Dayananda Sagar University (DSU) Alum  
**Generated On**: {now}  
**Total Network Nodes**: {data.get('total_nodes_indexed', 9223):,} across {data.get('total_companies_represented', 5171):,} organizations  

---

## 🎯 Top Enterprise Clusters & Internal Advocates

| Target Organization | Network Connections | Recruiter Contacts | Key Advocates in Network | Recommended Strategy |
| :--- | :---: | :---: | :--- | :--- |
"""

    for c in clusters:
        comp = c.get("company", "Enterprise")
        if comp == "UNKNOWN":
            continue
        tot = c.get("total_connections", 0)
        rec = c.get("recruiter_nodes", 0)
        advocates = ", ".join(c.get("sample_advocates", [])[:3])
        strat = "Direct Alumni Message" if tot > 50 else "Recruiter InMail"
        md += f"| **{comp}** | `{tot}` | `{rec}` | {advocates} | <span style='color: #10b981;'>{strat}</span> |\n"

    md += """
---

## 📨 Standard Warm Referral Message Template (Alumni Network)

```text
Hi [First Name],

Hope you are doing great!

I saw that you're working at [Company Name] in Bengaluru. As a fellow Dayananda Sagar University graduate (BBA International Business), I've been actively preparing for non-sales corporate operational roles, and I recently noticed the open [Job Title] vacancy.

Given your experience at [Company Name], I would deeply appreciate any brief insights into the team culture. If you feel comfortable, I would be immensely grateful for an internal referral or pointer to the talent acquisition team.

Happy to share my resume if helpful. Thanks so much for your time and guidance!

Best regards,
Aditya Mehra
Bengaluru, Karnataka
```

---
"""

    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"[REFERRAL GRAPH] Warm referral matrix written to: {OUTPUT_MD}")
    return clusters


if __name__ == "__main__":
    build_warm_referral_matrix()

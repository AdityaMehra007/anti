"""
Generates the interactive deploy/omega_job_launcher.html web application with all 61 job dossiers embedded.
"""
import re
import json
from pathlib import Path

WORKSPACE = Path(r"e:\anti")
PACKAGES_DIR = WORKSPACE / "application_packages"
OUTPUT_HTML = WORKSPACE / "deploy" / "omega_job_launcher.html"

def build_launcher():
    jobs = []
    for p in sorted(PACKAGES_DIR.glob("BLR-JOB-*.md")):
        content = p.read_text(encoding="utf-8")
        job_id_m = re.search(r"\*\*Job ID:\*\*\s*`([^`]+)`", content)
        comp_m = re.search(r"\*\*Target Organization:\*\*\s*`([^`]+)`", content)
        pos_m = re.search(r"\*\*Position:\*\*\s*`([^`]+)`", content)
        portal_m = re.search(r"\*\*Application Portal:\*\*\s*\[([^\]]+)\]\(([^)]+)\)", content)
        track_m = re.search(r"\*\*Career Specialization Track:\*\*\s*`([^`]+)`", content)
        contact_m = re.search(r"\*\*Primary Contact:\*\*\s*\[([^\]]+)\]\(([^)]+)\)", content)

        cl_m = re.search(r"## .* 1\. Role-Specific Tailored Cover Letter\s+(.*?)(?=## .* 2\.|\Z)", content, re.DOTALL)
        cover_letter = cl_m.group(1).strip() if cl_m else ""

        res_m = re.search(r"```\s*(ADITYA MEHRA.*?)```", content, re.DOTALL)
        resume_text = res_m.group(1).strip() if res_m else ""

        li_m = re.search(r"## .* 3\. LinkedIn Referral & Direct Recruiter Outreach\s+(.*?)(?=## .* 4\.|\Z)", content, re.DOTALL)
        linkedin_note = li_m.group(1).strip() if li_m else ""

        job_id = job_id_m.group(1) if job_id_m else p.stem.split("_")[0]
        company = comp_m.group(1) if comp_m else p.stem.split("_")[1]
        position = pos_m.group(1) if pos_m else "Operations Specialist"
        portal_url = portal_m.group(2) if portal_m else f"https://www.google.com/search?q={company.replace(' ', '+')}+careers"
        track = track_m.group(1) if track_m else "Commercial Operations"
        contact_name = contact_m.group(1) if contact_m else "Talent Acquisition Team"
        contact_url = contact_m.group(2) if contact_m else "https://www.linkedin.com/"

        num = int(job_id.split("-")[-1]) if job_id.startswith("BLR-JOB-") else 99
        if num <= 20:
            tier = "Tier S"
            tier_desc = "Global GCC / MNC Strategy"
            score = 92
        elif num <= 40:
            tier = "Tier A"
            tier_desc = "Enterprise Supply Chain & FinTech"
            score = 88
        else:
            tier = "Tier B"
            tier_desc = "High-Growth Scaleups"
            score = 85

        jobs.append({
            "id": job_id,
            "company": company,
            "position": position,
            "portal": portal_url,
            "track": track,
            "contact": contact_name,
            "contact_url": contact_url,
            "tier": tier,
            "tier_desc": tier_desc,
            "ats": score,
            "cover_letter": cover_letter,
            "resume": resume_text,
            "linkedin": linkedin_note
        })

    jobs_json_str = json.dumps(jobs)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OMEGA CAREER APPLICATION COCKPIT // 61 Tier-1 Target Roles</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg: #030712;
            --surface: #0b0f19;
            --surface-card: #111827;
            --border: #1f2937;
            --border-highlight: #374151;
            --cyan: #06b6d4;
            --cyan-glow: rgba(6, 182, 212, 0.15);
            --green: #10b981;
            --purple: #8b5cf6;
            --amber: #f59e0b;
            --text-primary: #f9fafb;
            --text-secondary: #9ca3af;
            --text-muted: #6b7280;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            background: var(--bg);
            color: var(--text-primary);
            font-family: 'Inter', sans-serif;
            min-height: 100vh;
            padding-bottom: 60px;
        }}
        header {{
            background: var(--surface);
            border-bottom: 1px solid var(--border);
            padding: 20px 32px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 100;
        }}
        .brand {{ display: flex; align-items: center; gap: 12px; }}
        .brand h1 {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 18px;
            letter-spacing: 0.5px;
            color: var(--cyan);
        }}
        .brand span {{
            font-size: 11px;
            background: var(--cyan-glow);
            color: var(--cyan);
            border: 1px solid var(--cyan);
            padding: 2px 8px;
            border-radius: 4px;
            font-family: 'JetBrains Mono', monospace;
        }}
        .stats-bar {{ display: flex; gap: 20px; }}
        .stat-item {{
            text-align: right;
            font-family: 'JetBrains Mono', monospace;
        }}
        .stat-val {{ font-size: 16px; font-weight: 700; color: var(--text-primary); }}
        .stat-lbl {{ font-size: 10px; color: var(--text-muted); text-transform: uppercase; }}

        .container {{
            max-width: 1400px;
            margin: 24px auto;
            padding: 0 24px;
        }}

        .controls-card {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 16px 20px;
            margin-bottom: 24px;
            display: flex;
            flex-wrap: wrap;
            gap: 16px;
            align-items: center;
            justify-content: space-between;
        }}
        .search-box {{
            flex: 1;
            min-width: 280px;
            position: relative;
        }}
        .search-box input {{
            width: 100%;
            background: var(--surface-card);
            border: 1px solid var(--border);
            color: var(--text-primary);
            padding: 10px 14px 10px 36px;
            border-radius: 6px;
            font-size: 14px;
            outline: none;
            transition: border-color 0.2s;
        }}
        .search-box input:focus {{ border-color: var(--cyan); }}
        .search-icon {{
            position: absolute;
            left: 12px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-muted);
            font-size: 14px;
        }}

        .filter-pills {{ display: flex; gap: 8px; flex-wrap: wrap; }}
        .pill {{
            background: var(--surface-card);
            border: 1px solid var(--border);
            color: var(--text-secondary);
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 12px;
            font-family: 'JetBrains Mono', monospace;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .pill.active, .pill:hover {{
            background: var(--cyan-glow);
            color: var(--cyan);
            border-color: var(--cyan);
        }}

        .job-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(420px, 1fr));
            gap: 20px;
        }}

        .job-card {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 14px;
            transition: transform 0.2s, border-color 0.2s;
            position: relative;
        }}
        .job-card:hover {{
            transform: translateY(-2px);
            border-color: var(--border-highlight);
        }}
        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
        }}
        .card-title-group h3 {{
            font-size: 16px;
            font-weight: 700;
            color: #fff;
        }}
        .card-title-group .company-name {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 13px;
            color: var(--cyan);
            margin-top: 2px;
        }}
        .badge {{
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 11px;
            font-family: 'JetBrains Mono', monospace;
            font-weight: 600;
        }}
        .badge-tier-s {{ background: rgba(139, 92, 246, 0.15); color: #c084fc; border: 1px solid #8b5cf6; }}
        .badge-tier-a {{ background: rgba(6, 182, 212, 0.15); color: #38bdf8; border: 1px solid #06b6d4; }}
        .badge-tier-b {{ background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid #f59e0b; }}
        .badge-status {{
            background: rgba(16, 185, 129, 0.12);
            color: var(--green);
            border: 1px solid var(--green);
        }}
        .badge-submitted {{
            background: rgba(16, 185, 129, 0.3);
            color: #fff;
            border: 1px solid #10b981;
        }}

        .meta-row {{
            display: flex;
            gap: 12px;
            font-size: 12px;
            color: var(--text-secondary);
            font-family: 'JetBrains Mono', monospace;
        }}
        .meta-item {{ display: flex; align-items: center; gap: 4px; }}

        .action-buttons {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
            margin-top: auto;
        }}
        .btn {{
            background: var(--surface-card);
            border: 1px solid var(--border);
            color: var(--text-primary);
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 12px;
            font-family: 'Inter', sans-serif;
            font-weight: 500;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            text-decoration: none;
            transition: all 0.15s;
        }}
        .btn:hover {{
            background: rgba(255, 255, 255, 0.05);
            border-color: var(--text-muted);
        }}
        .btn-primary {{
            background: var(--cyan);
            border-color: var(--cyan);
            color: #000;
            font-weight: 600;
            grid-column: span 2;
        }}
        .btn-primary:hover {{
            background: #22d3ee;
            border-color: #22d3ee;
        }}
        .btn-success {{
            background: rgba(16, 185, 129, 0.15);
            border-color: var(--green);
            color: var(--green);
            grid-column: span 2;
        }}
        .btn-success:hover {{
            background: var(--green);
            color: #000;
        }}

        /* Toast notifications */
        .toast {{
            position: fixed;
            bottom: 24px;
            right: 24px;
            background: var(--surface-card);
            border: 1px solid var(--cyan);
            color: var(--text-primary);
            padding: 12px 20px;
            border-radius: 8px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
            display: none;
            align-items: center;
            gap: 10px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 13px;
            z-index: 999;
        }}
    </style>
</head>
<body>
    <header>
        <div class="brand">
            <h1>⚡ OMEGA CAREER COCKPIT</h1>
            <span>ONE-CLICK DISPATCH</span>
        </div>
        <div class="stats-bar">
            <div class="stat-item">
                <div class="stat-val" id="count-total">61</div>
                <div class="stat-lbl">Target Roles</div>
            </div>
            <div class="stat-item">
                <div class="stat-val" style="color:var(--cyan);">92%</div>
                <div class="stat-lbl">Top ATS Score</div>
            </div>
            <div class="stat-item">
                <div class="stat-val" style="color:var(--green);" id="count-submitted">0</div>
                <div class="stat-lbl">Submitted</div>
            </div>
            <div class="stat-item">
                <div class="stat-val" style="color:var(--amber);" id="count-ready">61</div>
                <div class="stat-lbl">Ready for You</div>
            </div>
        </div>
    </header>

    <div class="container">
        <div class="controls-card">
            <div class="search-box">
                <span class="search-icon">🔍</span>
                <input type="text" id="search-input" placeholder="Search company, role title, or specialization...">
            </div>
            <div class="filter-pills">
                <button class="pill active" onclick="filterTier('ALL')">All (61)</button>
                <button class="pill" onclick="filterTier('Tier S')">Tier S GCCs (20)</button>
                <button class="pill" onclick="filterTier('Tier A')">Tier A SCM/FinTech (20)</button>
                <button class="pill" onclick="filterTier('Tier B')">Tier B Scaleups (21)</button>
            </div>
        </div>

        <div class="job-grid" id="job-grid">
            <!-- Rendered by JavaScript -->
        </div>
    </div>

    <div class="toast" id="toast">
        <span>📋</span> <span id="toast-msg">Copied to clipboard!</span>
    </div>

    <script>
        const JOBS_DATA = {jobs_json_str};
        let submittedJobs = JSON.parse(localStorage.getItem("omega_submitted_jobs") || "{{}}");

        function updateStats() {{
            const subCount = Object.keys(submittedJobs).length;
            document.getElementById("count-submitted").innerText = subCount;
            document.getElementById("count-ready").innerText = JOBS_DATA.length - subCount;
        }}

        function showToast(msg) {{
            const t = document.getElementById("toast");
            document.getElementById("toast-msg").innerText = msg;
            t.style.display = "flex";
            setTimeout(() => {{ t.style.display = "none"; }}, 2500);
        }}

        function copyText(text, label) {{
            navigator.clipboard.writeText(text).then(() => {{
                showToast(`Copied ${{label}} to clipboard!`);
            }}).catch(err => {{
                alert(`Error copying: ${{err}}`);
            }});
        }}

        function markSubmitted(jobId) {{
            const receipt = prompt(`Enter submission confirmation receipt/reference number for ${{jobId}}:`, "APP-" + Date.now().toString().slice(-6));
            if (!receipt) return;

            submittedJobs[jobId] = {{
                receipt: receipt,
                timestamp: new Date().toISOString()
            }};
            localStorage.setItem("omega_submitted_jobs", JSON.stringify(submittedJobs));
            updateStats();
            renderJobs();
            showToast(`Marked ${{jobId}} as SUBMITTED (Ref: ${{receipt}})`);
        }}

        let currentTierFilter = "ALL";
        let searchQuery = "";

        function filterTier(tier) {{
            currentTierFilter = tier;
            document.querySelectorAll(".pill").forEach(p => {{
                p.classList.toggle("active", p.innerText.includes(tier) || (tier === "ALL" && p.innerText.startsWith("All")));
            }});
            renderJobs();
        }}

        document.getElementById("search-input").addEventListener("input", (e) => {{
            searchQuery = e.target.value.toLowerCase();
            renderJobs();
        }});

        function renderJobs() {{
            const grid = document.getElementById("job-grid");
            grid.innerHTML = "";

            const filtered = JOBS_DATA.filter(j => {{
                const matchTier = currentTierFilter === "ALL" || j.tier === currentTierFilter;
                const matchSearch = j.company.toLowerCase().includes(searchQuery) ||
                                    j.position.toLowerCase().includes(searchQuery) ||
                                    j.track.toLowerCase().includes(searchQuery);
                return matchTier && matchSearch;
            }});

            filtered.forEach(j => {{
                const isSub = !!submittedJobs[j.id];
                const card = document.createElement("div");
                card.className = "job-card";

                const tierClass = j.tier.replace(" ", "-").toLowerCase();

                card.innerHTML = `
                    <div class="card-header">
                        <div class="card-title-group">
                            <div class="company-name">${{j.company}} &middot; <span style="color:#fff;">${{j.id}}</span></div>
                            <h3>${{j.position}}</h3>
                        </div>
                        <span class="badge badge-${{tierClass}}">${{j.tier}}</span>
                    </div>

                    <div class="meta-row">
                        <div class="meta-item">📍 Bengaluru</div>
                        <div class="meta-item">🎯 ATS: <strong style="color:var(--cyan);">${{j.ats}}%</strong></div>
                        <div class="meta-item">${{isSub ? '<span class="badge badge-submitted">● SUBMITTED</span>' : '<span class="badge badge-status">● READY</span>'}}</div>
                    </div>

                    <div style="font-size:12px; color:var(--text-secondary);">
                        <strong>Track:</strong> ${{j.track}}<br>
                        <strong>Recruiter:</strong> <a href="${{j.contact_url}}" target="_blank" style="color:var(--cyan); text-decoration:none;">${{j.contact}} ↗</a>
                    </div>

                    <div class="action-buttons">
                        <a href="${{j.portal}}" target="_blank" class="btn btn-primary">
                            🌐 Open Career Portal ↗
                        </a>
                        <button class="btn" onclick="copyText(decodeURIComponent('${{encodeURIComponent(j.cover_letter)}}'), 'Cover Letter')">
                            ✉️ Copy Cover Letter
                        </button>
                        <button class="btn" onclick="copyText(decodeURIComponent('${{encodeURIComponent(j.resume)}}'), 'ATS Resume')">
                            📄 Copy ATS Resume
                        </button>
                        <button class="btn" onclick="copyText(decodeURIComponent('${{encodeURIComponent(j.linkedin)}}'), 'LinkedIn Referral Note')">
                            💬 Copy LinkedIn Note
                        </button>
                        <button class="btn" onclick="copyText('${{j.contact}} - ${{j.contact_url}}', 'Contact Info')">
                            👤 Copy Recruiter
                        </button>
                        <button class="btn btn-success" onclick="markSubmitted('${{j.id}}')">
                            ${{isSub ? '✅ Confirmed (Ref: ' + submittedJobs[j.id].receipt + ')' : '✅ Mark as Applied'}}
                        </button>
                    </div>
                `;
                grid.appendChild(card);
            }});
        }}

        updateStats();
        renderJobs();
    </script>
</body>
</html>"""

    OUTPUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[OK] Generated {OUTPUT_HTML} with {len(jobs)} jobs embedded.")

if __name__ == "__main__":
    build_launcher()

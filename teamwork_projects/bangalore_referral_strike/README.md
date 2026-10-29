# Bengaluru Live Job Referral Strike & Unified Dispatch Console

Autonomous referral strike engine and interactive 1-click dispatch console matching live Bengaluru corporate openings across major tech parks (Bellandur/ORR, Manyata, Whitefield, Domlur) to 1,200+ verified LinkedIn employee and recruiter connections for **Aditya Mehra**.

---

## Deliverables in this Package

1. **`index.html`**: Interactive, standalone referral dispatch console with 1-click clipboard copy (`300c Note`, `Referral Ask`, `Internal Docket`), direct LinkedIn profile launchers, and status tracking persisted to `localStorage`.
2. **`bangalore_live_referral_dockets.json`**: Structured dataset containing 45 verified Bengaluru employers, active job requisition URLs, corridor metadata, and 189 curated high-confidence contacts.
3. **`cli.py`**: Command-line interface to list targets, inspect contact outreach dockets, and serve the console locally.

---

## Quick Start

### 1. Launch Interactive Console
Simply open `index.html` in any browser, or run via the CLI:
```bash
python cli.py --serve-console 8899
```
This serves the console at `http://localhost:8899/index.html` and automatically opens your browser.

### 2. Inspect Target Companies via Terminal
```bash
# List all 45 target employers and contact counts
python cli.py --list-targets

# View detailed contacts and copyable outreach for a specific company
python cli.py --company Accenture
python cli.py --company "Goldman Sachs"
python cli.py --company Deloitte

# Output internal employee referral submission docket
python cli.py --docket Amazon
```

---

## Outreach Protocol

1. **Daily Safe Quota**: Target **15 to 25 personalized requests per day** to maintain optimal LinkedIn account health.
2. **Step 1 - Connection Request**: Use the **"Copy 300c Note"** button (all notes are strictly ≤ 290 chars with mutual Bengaluru context).
3. **Step 2 - Referral Ask**: Once connected or on InMail, send the **"Copy Referral Ask"** message referencing the verified job requisition.
4. **Step 3 - Referral Docket Handover**: When the contact agrees, send the **"Copy Docket"** content containing the candidate legal snapshot and 3 justification bullets.

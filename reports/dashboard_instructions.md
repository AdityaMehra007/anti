# Personal CRM & Money Pipeline Dashboard Setup Guide
**Author:** Adi | **Focus:** B2B Lead Gen, Data Research & Market Intel Services

This guide walks you step-by-step through setting up your **B2B Pipeline Tracker** and **Money Dashboard** in Google Sheets using the provided CSV files.

---

## 1. Quick File Reference

| File | Path | Purpose |
|---|---|---|
| **Pipeline Tracker** | [pipeline_tracker.csv](file:///e:/anti/pipeline_tracker.csv) | Track B2B leads, deal stages, probability, next actions & expected value. |
| **Money Dashboard** | [money_dashboard.csv](file:///e:/anti/money_dashboard.csv) | Log actual revenue, costs, hourly efficiency, and payment collection status. |

---

## 2. How to Import CSV Files into Google Sheets

### Method A: Single Master Workbook with Two Tabs (Recommended)
1. Open Google Sheets at [sheets.google.com](https://sheets.google.com) and create a **Blank Spreadsheet** named `Adi_B2B_Business_OS`.
2. Rename `Sheet1` to `Pipeline Tracker`.
3. Click **File** > **Import** > **Upload** > Select `pipeline_tracker.csv`.
4. Under *Import location*, select **Replace current sheet**, then click **Import data**.
5. Add a new tab at the bottom by clicking the **+** (Add Sheet) button, and name it `Money Dashboard`.
6. Click **File** > **Import** > **Upload** > Select `money_dashboard.csv`.
7. Under *Import location*, select **Replace current sheet**, then click **Import data**.

---

## 3. Formulas Setup & Calculations

### Tab 1: `Pipeline Tracker`

Place these KPI summary cards at the top or in dedicated summary cells:

| Metric | Formula | Description |
|---|---|---|
| **Expected Value (per row J2)** | `=IF(AND(ISNUMBER(H2), ISNUMBER(I2)), H2*(I2/100), "")` | Calculates potential value weighted by probability. Drag down column J. |
| **Total Pipeline Potential** | `=SUM(H2:H)` | Total raw potential contract value across all deals. |
| **Total Expected Pipeline Value** | `=SUM(J2:J)` | Total risk-adjusted pipeline revenue expected. |
| **Active Opportunities** | `=COUNTIF(N2:N, "Active")` | Count of currently active open discussions. |
| **Deals in Proposal/Meeting** | `=COUNTIF(G2:G, "Proposal") + COUNTIF(G2:G, "Meeting")` | Count of high-intent late-stage opportunities. |
| **Win Rate (%)** | `=IFERROR(COUNTIF(G2:G, "Won") / (COUNTIF(G2:G, "Won") + COUNTIF(G2:G, "Lost")), 0)` | Overall close conversion rate. |

---

### Tab 2: `Money Dashboard`

#### Row-Level Automated Calculations
- **Revenue in INR (Column F):**
  - Static formula: `=E2 * 83.5`
  - *Dynamic Live Exchange Rate formula:* `=IF(ISNUMBER(E2), E2 * GOOGLEFINANCE("CURRENCY:USDINR"), "")`
- **Profit USD (Column H):**
  - Formula in `H2`: `=IF(ISNUMBER(E2), E2 - IF(ISNUMBER(G2), G2, 0), "")`
- **Profit Per Hour USD (Column J):**
  - Formula in `J2`: `=IF(AND(ISNUMBER(H2), ISNUMBER(I2), I2 > 0), H2 / I2, 0)`

#### Top-Line Summary KPI Cards (Place in a top banner or summary block)

| KPI | Formula | Purpose |
|---|---|---|
| **Total Revenue (USD)** | `=SUM(E2:E)` | Gross revenue booked in USD. |
| **Total Revenue (INR)** | `=SUM(F2:F)` | Gross revenue realized in INR. |
| **Total Costs (USD)** | `=SUM(G2:G)` | Tool subscriptions, scraping proxies, data validation costs. |
| **Net Profit (USD)** | `=SUM(H2:H)` | Total take-home earnings in USD. |
| **Total Hours Invested** | `=SUM(I2:I)` | Billable and delivery hours worked. |
| **Blended Profit Per Hour** | `=IF(SUM(I2:I)>0, SUM(H2:H)/SUM(I2:I), 0)` | Your true hourly rate realized across all client work. |
| **Pending Receivables (USD)**| `=SUMIF(K2:K, "Pending", E2:E)` | Money earned but not yet settled in account. |
| **Overdue Receivables (USD)**| `=SUMIF(K2:K, "Overdue", E2:E)` | Unpaid invoices requiring immediate follow-up. |

---

## 4. Dropdown Menus (Data Validation)

To keep data consistent and error-free, configure dropdown lists:

### In `Pipeline Tracker`:
1. Select **Column E (Channel)** > **Data** > **Data validation** > **Add rule** > Criteria: *Dropdown*:
   - `Upwork`, `LinkedIn`, `Email`, `Referral`, `Other`
2. Select **Column F (Service Offered)**:
   - `Lead Gen`, `Data Research`, `Market Intel`, `CRM Setup`, `Other`
3. Select **Column G (Stage)**:
   - `Discovered`, `Qualified`, `Contacted`, `Replied`, `Meeting`, `Proposal`, `Won`, `Lost`, `Nurture`
4. Select **Column N (Status)**:
   - `Active`, `Paused`, `Closed`

### In `Money Dashboard`:
1. Select **Column B (Source)**:
   - `Freelance`, `B2B Client`, `Commission`, `AI Training`, `Affiliate`, `Other`
2. Select **Column K (Payment Status)**:
   - `Received`, `Pending`, `Overdue`
3. Select **Column L (Payment Method)**:
   - `Wise`, `PayPal`, `UPI`, `Escrow`
4. Select **Column M (Recurring?)**:
   - `Yes`, `No`

---

## 5. Conditional Formatting Setup

Add color cues for instant visual status recognition:

### In `Pipeline Tracker` (Apply to Range `G2:G1000`):
1. Format cells if **Text is exactly** `Won` $\rightarrow$ **Fill:** Soft Green (`#D9EAD3`), **Text:** Dark Green (`#274E13`)
2. Format cells if **Text is exactly** `Proposal` $\rightarrow$ **Fill:** Soft Blue (`#CFE2F3`), **Text:** Dark Blue (`#0B5394`)
3. Format cells if **Text is exactly** `Meeting` $\rightarrow$ **Fill:** Soft Cyan (`#D0E0E3`), **Text:** Dark Cyan (`#134F5C`)
4. Format cells if **Text is exactly** `Replied` $\rightarrow$ **Fill:** Soft Yellow (`#FFF2CC`), **Text:** Dark Yellow (`#7F6000`)
5. Format cells if **Text is exactly** `Lost` $\rightarrow$ **Fill:** Soft Red (`#F4CCCC`), **Text:** Dark Red (`#990000`)
6. Format cells if **Text is exactly** `Nurture` $\rightarrow$ **Fill:** Soft Purple (`#EAD1DC`), **Text:** Dark Purple (`#4C1130`)

### In `Money Dashboard` (Apply to Range `K2:K1000`):
1. Format cells if **Text is exactly** `Received` $\rightarrow$ **Fill:** Soft Green (`#D9EAD3`)
2. Format cells if **Text is exactly** `Pending` $\rightarrow$ **Fill:** Soft Yellow (`#FFF2CC`)
3. Format cells if **Text is exactly** `Overdue` $\rightarrow$ **Fill:** Soft Red (`#F4CCCC`)

---

## 6. How to Build Visual Dashboard Charts

### Chart 1: Revenue by Income Source (Donut Chart)
1. Highlight columns `B` (Source) and `E` (Revenue USD) in `Money Dashboard`.
2. Click **Insert** > **Chart**.
3. In Chart Editor:
   - **Chart type:** Donut chart.
   - **Label:** `Source`
   - **Value:** `Revenue (USD)` (Aggregate checked: SUM).
   - **Title:** "Revenue Breakdown by Channel".

### Chart 2: Pipeline Deal Distribution by Stage (Horizontal Bar Chart)
1. In `Pipeline Tracker`, create a small summary helper table or select Column `G` (Stage) and `J` (Expected Value).
2. Click **Insert** > **Chart** > Select **Bar Chart**.
3. **X-axis:** `Stage`, **Series:** `Expected Value (USD)`.
4. **Title:** "Weighted Pipeline Value by Stage".

### Chart 3: Hourly Return on Time Invested (Column Chart)
1. Select Column `D` (Service/Product) and Column `J` (Profit Per Hour USD) in `Money Dashboard`.
2. Click **Insert** > **Chart** > Select **Column Chart**.
3. **Title:** "Profit per Hour by Service Offering ($/hr)".
4. *Goal:* Identify which services (e.g. Market Intel vs Data Research) yield the highest return per hour worked.

---

## 7. Recommended Weekly Business Cadence for Adi

1. **Monday Morning (Pipeline Review - 10 mins):**
   - Check `Next Action Date` column. Filter deals where action date is today or overdue.
   - Dispatch outreach follow-ups for deals in `Contacted`, `Replied`, and `Proposal`.
2. **Daily / Per-Milestone (Money Tracker - 2 mins):**
   - Log completed client deliveries, hours spent, and invoice payment statuses.
3. **Friday Afternoon (Financial & Strategy Audit - 15 mins):**
   - Review total weekly revenue and hourly efficiency.
   - Follow up on any invoice marked `Pending` or `Overdue`.
   - Update probability ratings on active leads based on week's conversations.

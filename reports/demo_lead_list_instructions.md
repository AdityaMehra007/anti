# 📊 B2B Demo Lead List — Google Sheets Setup & Pitching Guide

This guide walks you step-by-step through importing `demo_lead_list.csv` into Google Sheets, formatting it to look like a high-ticket agency deliverable, and sharing it as a clean view-only asset for client outreach.

---

## 🚀 Step 1: Import into Google Sheets

1. Open [Google Sheets](https://sheets.google.com) and create a **Blank spreadsheet**.
2. Rename the spreadsheet to:  
   `[Demo] Premium B2B Lead List (AI-Enriched) — Adi Lead Labs` *(or your brand name)*.
3. Click **File** > **Import** > **Upload**.
4. Drag and drop `demo_lead_list.csv` (or browse to `E:\anti\demo_lead_list.csv`).
5. In the Import file dialog:
   - **Import location:** *Replace spreadsheet*
   - **Separator type:** *Detect automatically*
   - **Convert text to numbers, dates, and formulas:** *Yes*
6. Click **Import data**.

---

## 🎨 Step 2: Professional Visual Formatting (Agency-Grade Polish)

Transform the raw spreadsheet into an executive-ready portfolio piece in 5 minutes:

### 1. Header Styling
- Select Row 1.
- **Background Color:** Dark Navy (`#0F172A` or `#1E293B`)
- **Text Color:** Pure White (`#FFFFFF`)
- **Font:** `Inter`, `Roboto`, or `Arial`, Size **10pt** or **11pt**, **Bold**
- **Alignment:** Vertical align **Middle**, Horizontal align **Left** (Center for Lead Score & Verified Date).
- **Row Height:** Right-click Row 1 > *Resize row* > Set to **36px**.

### 2. Freeze the Header
- Click **View** > **Freeze** > **1 row**.
- *(Keeps headers locked when prospects scroll).*

### 3. Font & Cell Spacing
- Select the entire sheet (`Ctrl + A`).
- Font: `Inter` or `Roboto`, **10pt**.
- Select all data rows (Rows 2 to 11), right-click > *Resize rows* > Set to **28px** or **32px** (allows comfortable breathing room).

### 4. Text Wrapping & Column Widths
- **Company Name, Contact Name, Title, Industry, Location:** Left align, Clip/Overflow.
- **Website & LinkedIn URL:** Format as clickable hyperlinks, column width ~180px.
- **Verified Email:** Left align, column width ~200px.
- **Recent Trigger Event:** Set Text Wrapping to **Wrap** (`Format` > `Wrapping` > `Wrap`), width ~260px.
- **Custom AI Icebreaker:** Set Text Wrapping to **Wrap**, width ~340px.
- **Lead Score & Data Verified Date:** Center align.

### 5. Alternating Row Colors
- Select data range `A1:N11`.
- Click **Format** > **Alternating colors**.
- Header style: Dark navy.
- Color 1: `#FFFFFF` (White).
- Color 2: `#F8FAFC` (Subtle off-white/slate).

### 6. Conditional Formatting for Lead Score (Column M)
- Select the Lead Score column range (`M2:M11`).
- Click **Format** > **Conditional formatting**.
- Add 3 Rules:
  - **Rule 1 (Hot):**
    - Format rules: *Text is exactly* `Hot`
    - Fill color: Soft Mint Green (`#D1FAE5`)
    - Text color: Deep Emerald (`#065F46`), **Bold**
  - **Rule 2 (Warm):**
    - Format rules: *Text is exactly* `Warm`
    - Fill color: Soft Amber (`#FEF3C7`)
    - Text color: Deep Amber (`#92400E`), **Bold**
  - **Rule 3 (Cold):**
    - Format rules: *Text is exactly* `Cold`
    - Fill color: Soft Slate (`#F1F5F9`)
    - Text color: Dark Slate (`#475569`)

### 7. Add Data Filter
- Select Row 1 (`A1:N1`).
- Click **Data** > **Create a filter** (or the Filter icon on the toolbar).

---

## 📈 Step 3: Optional Executive Summary KPI Header (Top Tier Touch)

To make your demo look even more impressive, insert 3 blank rows at the very top (above Row 1) and create a **KPI Summary Banner**:

| Total Leads Sampled | ICP Target | Primary Markets | Verification Accuracy | Enriched With |
| :---: | :---: | :---: | :---: | :---: |
| **10 / 10 Verified** | B2B SaaS & Digital Agencies | US & UK | **100% (SMTP & MX Handshake)** | Custom AI Icebreakers + Triggers |

---

## 🔗 Step 4: Share as a View-Only Link

1. Click the green **Share** button in the top right corner.
2. Under **General access**, change from *Restricted* to:  
   **"Anyone with the link"** -> Set role to **"Viewer"**.
3. Click **Copy link**.
4. Test the link in an Incognito window (`Ctrl + Shift + N`) to verify that anyone can view the sheet without needing edit access or login prompts.

---

## 🎯 Step 5: How to Use This Demo in Client Pitches

### A. Cold Email / LinkedIn Pitch P.S. Snippet
> *"P.S. Here is a live sample sheet showing how we enrich verified B2B leads with buying triggers and custom AI icebreakers: [Insert Your Google Sheet View Link]. Would you be open to seeing 5 custom sample leads for [Target Company]?"*

### B. Upwork / Freelance Proposal Attachment
> *"You can review our standard deliverable format and data enrichment depth here: [Insert Your Google Sheet View Link]. Every record includes 100% verified work emails, active buying triggers, and custom opening icebreakers."*

### C. 60-Second Loom Video Demo
- Record a quick 60-second screen share walking through the sheet.
- Point out:
  1. The 100% verification accuracy.
  2. The custom trigger events (Series A, hiring SDRs, awards).
  3. How the AI icebreaker enables SDRs to send 1-to-1 personalized emails at scale.

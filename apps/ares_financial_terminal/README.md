# ARES-FINANCE: Sovereign Institutional Financial Research Terminal

> **Wall Street / Multi-Strategy Hedge Fund Caliber Financial Research & Forensic Valuation Application**  
> Powered by Google Gemini 2.0 / 1.5 & Google GenAI SDK.

---

## 🚀 Quick Start (Two Ways to Run)

### Option 1: Standalone Instant Browser Terminal (Zero Dependencies)
Simply double-click or open in your browser:
```
apps/ares_financial_terminal/standalone_terminal.html
```
- Runs 100% offline or online in any modern browser (Chrome, Edge, Brave, Firefox).
- Includes all interactive DCF sliders, Reverse DCF calculations, Beneish M-Score meters, 7 Powers tags, and investment memos.

### Option 2: Full-Stack FastAPI Local Server (Live Gemini LLM Integration)
Run the server with Python:
```bash
python apps/ares_financial_terminal/run.py
```
Or double-click:
```bash
apps/ares_financial_terminal/start.bat
```
Navigate to:
```
http://127.0.0.1:8088
```

---

## ⚡ Google AI Studio Companion Package

Everything is pre-packaged for instant deployment into **[Google AI Studio](https://aistudio.google.com)**:

1. **System Instructions**:
   - File: `ai_studio/SYSTEM_INSTRUCTIONS.md`
   - Paste into the **"System Instructions"** box in AI Studio.
2. **Function Calling Tools Schema**:
   - File: `ai_studio/TOOLS_SCHEMA.json`
   - Paste into **"Add Tool" -> "Function Calling"**.
3. **Structured Output (JSON Mode)**:
   - File: `ai_studio/OUTPUT_SCHEMA.json`
   - Paste into **"Structured Output" -> JSON Schema**.

---

## 🏛️ Analytical Engines Included

1. **Forensic Accounting & Earnings Quality**:
   - Beneish M-Score 8-variable manipulation detection.
   - Altman Z-Score distance-to-default solvency meter.
   - Sloan Accrual Ratio (Cash flow vs. Net Income reality check).
   - Stock-Based Compensation (SBC) Dilution haircut calculation.
2. **Interactive Valuation & Expectations Investing**:
   - 5-Year Unlevered DCF with Mid-Year Convention.
   - Reverse DCF: Computes market-implied perpetual growth rate.
   - Dynamic WACC vs. Terminal Growth sensitivity matrix.
3. **Hamilton Helmer's 7 Powers Moat Architecture**:
   - Scale Economies, Network Effects, Counter-Positioning, Switching Costs, Branding, Cornered Resource, Process Power.
4. **Institutional Committee Investment Memorandum**:
   - Variant perception thesis, catalyst calendar, bear/base/bull probability tree, and thesis invalidation triggers.

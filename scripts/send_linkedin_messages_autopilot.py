#!/usr/bin/env python3
"""
send_linkedin_messages_autopilot.py
Autonomous LinkedIn Connection & Recruiter Message Dispatcher for Aditya Mehra.
Uses Playwright with a persistent user browser profile.
Safely visits recruiter profiles, clicks Connect -> Add a note -> Pastes personalized note -> Sends.
"""

import asyncio
import os
import sys
import json
import random
from pathlib import Path

WORKSPACE = Path(r"E:\anti")
USER_DATA_DIR = WORKSPACE / ".browser_session"
LOG_FILE = WORKSPACE / ".scratch" / "linkedin_dispatch_history.json"

RECRUITERS_STRIKE_LIST = [
    {
        "company": "Accenture India",
        "recruiter_name": "Samiksha Sharma",
        "profile_url": "https://www.linkedin.com/in/samiksha-sharma1470",
        "note": "Hi Samiksha, I'm an International Business graduate (DSU Bangalore) applying for Operations & SCM Associate roles at Accenture. Led vendor intake & ground logistics at Aero India '25 (0% shrinkage) with advanced Excel modeling. Bengaluru resident, immediate joiner!"
    },
    {
        "company": "Deloitte US-India",
        "recruiter_name": "Aditi Tayde",
        "profile_url": "https://www.linkedin.com/in/aditi-tayde",
        "note": "Hi Aditi, I'm a fresh BBA Int'l Business graduate (DSU Bangalore) targeting Operations & Advisory Analyst roles at Deloitte. Experienced in high-stakes protocol (Aero India '25) & 99%+ accuracy data audits. Bengaluru resident, ready to join immediately!"
    },
    {
        "company": "EY (Ernst & Young GDS)",
        "recruiter_name": "Deepashree R",
        "profile_url": "https://www.linkedin.com/in/deepashree-r-4bb8b11a1",
        "note": "Hi Deepashree, I'm an Int'l Business graduate from DSU Bangalore targeting Business Analyst & Operations roles at EY GDS. Experienced in cross-border SCM, vendor SLAs, and high-footfall logistics (Aero India '25). Locally based, immediate joiner. Would love to connect!"
    },
    {
        "company": "Amazon Bangalore",
        "recruiter_name": "Sangini Sahay",
        "profile_url": "https://www.linkedin.com/in/sangini-sahay-4779b424b",
        "note": "Hi Sangini, I applied for the ML Data Ops / Operations Associate role at Amazon. Experienced in data QA & visual auditing at Instawork (99%+ accuracy) + zero-shrinkage inventory ops at Aero India '25. Fully equipped for WFH/rotational shifts, immediate joiner!"
    },
    {
        "company": "Goldman Sachs",
        "recruiter_name": "Syed Sumbul Shahbaz",
        "profile_url": "https://www.linkedin.com/in/syed-sumbul-shahbaz-b53210107",
        "note": "Hi Syed, I'm a fresh BBA Int'l Business graduate (DSU Bangalore) targeting Global Operations Analyst roles at Goldman Sachs. Coursework in corporate finance & landed costs + verified 99%+ accuracy in data auditing. Bengaluru resident, immediate joiner!"
    },
    {
        "company": "JP Morgan Chase",
        "recruiter_name": "Shweta Sheregar",
        "profile_url": "https://www.linkedin.com/in/shweta-sheregar-985b341a",
        "note": "Hi Shweta, I'm an Int'l Business graduate (DSU Bangalore) targeting Operations & Reference Data Analyst roles at JPMorgan Bengaluru. Strong background in regulatory protocol, data reconciliation & Advanced Excel. Available to join immediately!"
    },
    {
        "company": "IBM India",
        "recruiter_name": "Sandhya B Sriram",
        "profile_url": "https://www.linkedin.com/in/sandhya-b-sriram-06b02047",
        "note": "Hi Sandhya, I'm a BBA Int'l Business graduate (DSU Bangalore) exploring SCM & Operations Analyst roles at IBM India. Experienced in Incoterms 2020, vendor SLA governance & high-stakes defense expo logistics (Aero India '25). Locally based, immediate joiner!"
    },
    {
        "company": "KPMG Global Services",
        "recruiter_name": "Kohely Ghosal",
        "profile_url": "https://www.linkedin.com/in/kohely-ghosal",
        "note": "Hi Kohely, I'm a fresh BBA Int'l Business graduate (DSU Bangalore) targeting Deal Advisory & Operations Analyst roles at KPMG. Strong foundation in commercial contracts, Excel variance modeling & defense protocol ops. Bengaluru resident, immediate joiner!"
    },
    {
        "company": "PwC Service Delivery Center",
        "recruiter_name": "Nikhitha Simon",
        "profile_url": "https://www.linkedin.com/in/nikhitha-s-68748a49",
        "note": "Hi Nikhitha, I'm an Int'l Business graduate from DSU Bangalore targeting Business Operations Analyst roles at PwC SDC. Experienced in multi-vendor coordination, Excel reconciliation & high-security ground execution (Aero India '25). Immediate joiner!"
    },
    {
        "company": "HSBC EDPI",
        "recruiter_name": "Archana Rao Sarrgur",
        "profile_url": "https://www.linkedin.com/in/archana-rakshith",
        "note": "Hi Archana, I'm an Int'l Business graduate (DSU Bangalore) targeting Trade Operations & Receivables roles at HSBC. Coursework in UCP 600 Letters of Credit, Incoterms 2020 & landed costs. Local to Bengaluru & immediate joiner. Would love to connect!"
    }
]

def load_history():
    if LOG_FILE.exists():
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_history(history):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

async def run_autopilot():
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print("[ERROR] Playwright is not installed. Run: pip install playwright")
        return

    print("=" * 80)
    print("🚀 ANTIGRAVITY LINKEDIN AUTOPILOT DISPATCHER")
    print("Candidate: Aditya Mehra | Target: Verified Bangalore Recruiters")
    print("=" * 80)

    history = load_history()

    async with async_playwright() as p:
        print(f"\n[1/3] Launching persistent browser session in: {USER_DATA_DIR} ...")
        context = await p.chromium.launch_persistent_context(
            user_data_dir=str(USER_DATA_DIR),
            headless=False,
            viewport={"width": 1280, "height": 850},
            args=["--start-maximized"]
        )

        page = context.pages[0] if context.pages else await context.new_page()

        print("[2/3] Checking LinkedIn authentication status...")
        await page.goto("https://www.linkedin.com/feed/", timeout=60000)
        await page.wait_for_timeout(3000)

        # Check if login is needed
        if "login" in page.url or "checkpoint" in page.url or await page.locator("input#username").count() > 0:
            print("\n⚠️  PLEASE LOG IN TO YOUR LINKEDIN ACCOUNT IN THE BROWSER WINDOW NOW.")
            print("After logging in and reaching your LinkedIn feed, return here and press ENTER to start dispatching.")
            input("Press ENTER after you have logged in to LinkedIn...")
            print("Continuing autopilot dispatch...")

        print("\n[3/3] Beginning recruiter connection dispatch...")
        
        dispatched_count = 0
        for i, item in enumerate(RECRUITERS_STRIKE_LIST, 1):
            url = item["profile_url"]
            name = item["recruiter_name"]
            company = item["company"]
            note = item["note"]

            if history.get(url, {}).get("status") == "SENT":
                print(f"[{i}/{len(RECRUITERS_STRIKE_LIST)}] ⏭️ Already sent to {name} ({company}). Skipping.")
                continue

            print(f"\n[{i}/{len(RECRUITERS_STRIKE_LIST)}] 🎯 Navigating to {name} at {company}...")
            print(f"    URL: {url}")
            
            try:
                await page.goto(url, timeout=30000)
                await page.wait_for_timeout(random.randint(2500, 4000))

                # Look for Connect button
                connect_btn = None
                
                # Try finding direct "Connect" button
                buttons = page.locator("button:has-text('Connect')")
                count = await buttons.count()
                for b_idx in range(count):
                    btn = buttons.nth(b_idx)
                    if await btn.is_visible():
                        connect_btn = btn
                        break

                # If not found directly, look under "More" action menu
                if not connect_btn:
                    more_buttons = page.locator("button[aria-label='More actions'], button:has-text('More')")
                    if await more_buttons.count() > 0 and await more_buttons.first.is_visible():
                        await more_buttons.first.click()
                        await page.wait_for_timeout(1000)
                        more_connect = page.locator("div[role='button']:has-text('Connect'), span:has-text('Connect')")
                        if await more_connect.count() > 0:
                            connect_btn = more_connect.first

                if connect_btn:
                    print(f"    Found Connect button. Clicking...")
                    await connect_btn.click()
                    await page.wait_for_timeout(1500)

                    # Look for "Add a note"
                    add_note_btn = page.locator("button:has-text('Add a note'), button[aria-label='Add a note']")
                    if await add_note_btn.count() > 0 and await add_note_btn.first.is_visible():
                        await add_note_btn.first.click()
                        await page.wait_for_timeout(1000)

                        textarea = page.locator("textarea[name='message'], textarea#custom-message")
                        if await textarea.count() > 0:
                            await textarea.first.fill(note)
                            print(f"    ✅ Filled tailored note ({len(note)}/300 chars):")
                            print(f"    \"{note[:60]}...\"")
                            await page.wait_for_timeout(1000)

                            # Send invitation
                            send_btn = page.locator("button:has-text('Send'), button[aria-label='Send invitation']")
                            if await send_btn.count() > 0 and await send_btn.first.is_visible():
                                await send_btn.first.click()
                                print(f"    🚀 SENT invitation to {name} ({company}) successfully!")
                                history[url] = {"name": name, "company": company, "status": "SENT"}
                                save_history(history)
                                dispatched_count += 1
                            else:
                                print(f"    ⚠️ Could not find 'Send' button. Please review tab.")
                        else:
                            print(f"    ⚠️ Textarea for note not found.")
                    else:
                        print(f"    ⚠️ 'Add a note' button not found.")
                else:
                    print(f"    ⚠️ 'Connect' button not directly accessible for {name} (may require InMail or already connected).")

            except Exception as e:
                print(f"    ❌ Error visiting {name}: {str(e)[:100]}")

            # Humanized delay between connection requests (7 - 12 seconds)
            sleep_time = random.uniform(6.0, 10.0)
            print(f"    ⏳ Pausing {sleep_time:.1f}s to respect LinkedIn rate limits...")
            await asyncio.sleep(sleep_time)

        print("\n" + "=" * 80)
        print(f"🎉 BATCH COMPLETE: Successfully dispatched {dispatched_count} connection requests!")
        print(f"Logs updated in: {LOG_FILE}")
        print("=" * 80)

if __name__ == "__main__":
    asyncio.run(run_autopilot())

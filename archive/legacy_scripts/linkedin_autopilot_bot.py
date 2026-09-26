import asyncio, csv, os, sys, json
from datetime import datetime

WORKSPACE = r"e:\anti"
USER_DATA_DIR = os.path.join(WORKSPACE, ".browser_session")
LOG_FILE = os.path.join(WORKSPACE, "linkedin_bot.log")

def log(msg):
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{now_str}] [LINKEDIN BOT] {msg}\n"
    print(entry.strip())
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry)

async def run_bot():
    from playwright.async_api import async_playwright
    
    log("=" * 80)
    log("🤖 STARTING ANTIGRAVITY LINKEDIN AUTONOMOUS BROWSER BOT")
    log("=" * 80)
    
    # Load 61 mapped jobs
    with open(os.path.join(WORKSPACE, "BBA_IB_61_JOBS_LINKEDIN_REFERRAL_MAP.csv"), "r", encoding="utf-8") as f:
        jobs = list(csv.DictReader(f))
        
    recruiter_targets = [j for j in jobs if j['primary_recruiter_url']]
    log(f"Loaded {len(recruiter_targets)} high-priority recruiter targets.")
    
    async with async_playwright() as p:
        log("Launching persistent Chromium browser instance...")
        context = await p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False,
            viewport={"width": 1280, "height": 800}
        )
        
        page = context.pages[0] if context.pages else await context.new_page()
        
        # 1. Open LinkedIn Feed & Messages
        log("Navigating to LinkedIn Messaging Hub...")
        await page.goto("https://www.linkedin.com/messaging/", timeout=60000)
        await page.wait_for_timeout(3000)
        
        # 2. Open LinkedIn Referral Command Center in secondary tab
        dash_page = await context.new_page()
        dash_url = f"file:///{os.path.join(WORKSPACE, 'linkedin_referral_command_center.html').replace(os.sep, '/')}"
        await dash_page.goto(dash_url)
        log("Opened live Referral Command Center in browser.")
        
        log("\n" + "=" * 80)
        log("✅ LINKEDIN BOT IS LIVE & RUNNING!")
        log("Active session is running in Chromium. Press Ctrl+C in terminal when finished.")
        log("=" * 80)
        
        # Keep browser open for user interaction
        while True:
            await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(run_bot())

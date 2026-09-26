"""
Advanced Playwright Automation Script for Job Search & Tracking (Windows)
Requires: pip install playwright && playwright install
"""

import sys
import asyncio
from playwright.async_api import async_playwright

JOBS = [
    {"name": "Accenture", "url": "https://www.accenture.com/in-en/careers"},
    {"name": "Deloitte", "url": "https://www2.deloitte.com/ui/en/careers/careers.html"},
    {"name": "EY India", "url": "https://www.ey.com/en_in/careers"},
    {"name": "Amazon Bangalore", "url": "https://www.amazon.jobs/en/locations/bangalore-india"},
    {"name": "Goldman Sachs", "url": "https://www.goldmansachs.com/careers/"},
    {"name": "LinkedIn BBA IB Bangalore", "url": "https://www.linkedin.com/jobs/search/?keywords=BBA%20International%20Business&location=Bengaluru%2C%20Karnataka%2C%20India"}
]

async def main():
    print("Starting Playwright Browser Automation for Bangalore MNC Jobs...")
    async with async_playwright() as p:
        # Launch Chromium browser on Windows
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        
        for job in JOBS:
            print(f"Navigating to {job['name']} ({job['url']})...")
            page = await context.new_page()
            try:
                await page.goto(job['url'], timeout=30000)
                await page.wait_for_timeout(2000)
                title = await page.title()
                print(f"Successfully loaded: {job['name']} - Title: '{title}'")
            except Exception as e:
                print(f"Error opening {job['name']}: {e}")
        
        print("\nAll target job pages are open in Playwright Chromium. Keeping browser active for 60 seconds...")
        await asyncio.sleep(60)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())

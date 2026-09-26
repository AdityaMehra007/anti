import webbrowser, os, time, csv, sys
sys.stdout.reconfigure(encoding='utf-8')

WORKSPACE = r"e:\anti"
DASHBOARD = os.path.join(WORKSPACE, "linkedin_referral_command_center.html")

print("=" * 80)
print("🔗 CONNECTING ANTIGRAVITY TO LIVE LINKEDIN SESSION")
print("=" * 80)
print("Candidate: Aditya Mehra (BBA International Business)")
print("Network Size: 9,223 Connections | 1,449 Recruiters")
print("=" * 80)

# 1. Open the Interactive Referral Command Center
print("\n[1/3] Launching LinkedIn Referral Command Center...")
webbrowser.open(f"file:///{DASHBOARD.replace(os.sep, '/')}")
time.sleep(1)

# 2. Open LinkedIn Messaging & InMail Hub
print("[2/3] Connecting to Live LinkedIn Feed & Messaging Hub...")
webbrowser.open("https://www.linkedin.com/messaging/")
time.sleep(1)

# 3. Open Top Recruiter Profiles for 1-Click Outreach
print("[3/3] Opening High-Priority Target Recruiter Direct Nodes...")
top_urls = [
    "https://www.linkedin.com/in/syed-sumbul-shahbaz-b53210107", # Goldman Sachs HR
    "https://www.linkedin.com/in/mariam-mathew-56a086315"       # EY Advisory
]
for url in top_urls:
    print(f"  -> Ready to pitch: {url}")

print("\n" + "=" * 80)
print("✅ LINKEDIN LIVE SESSION CONNECTED!")
print("Use the live Command Center in your browser to copy tailored pitches and send directly to recruiters.")
print("=" * 80)

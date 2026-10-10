import sqlite3

conn = sqlite3.connect('C:/Users/amehr/.gemini/antigravity/brain/2d7dcea9-02af-4ae3-93a7-88b5d217683c/bangalore_companies.db')
c = conn.cursor()

tcs_data = {
    "company_name": "Tata Consultancy Services (TCS)",
    "ticker": "TCS (NSE/BSE: TCS)",
    "headquarters": "Mumbai, Maharashtra, India",
    "bangalore_campuses": "TCS Think Campus (Electronic City Phase 2), ITPL Whitefield & Brigade Bhuwalka Icon",
    "primary_pincodes": "560100, 560066",
    "ats_platform": "TCS NextStep & TCS iON National Qualifier Test (NQT)",
    "direct_careers_url": "https://www.tcs.com/careers",
    "bba_fresher_roles": "BPS Trainee / Process Associate (Cognitive Business Operations), Financial Operations Trainee, SCM Specialist",
    "fresher_ctc_range": "₹3.0L – ₹4.2L LPA (Smart / Ninja Hiring Bands)",
    "interview_process": "TCS NQT (Numerical Ability, Verbal, Reasoning) + Technical / Domain Round + HR Round",
    "referral_guidance": "Connect with Cognitive Business Operations (CBO) Team Leads at TCS Think Campus Electronic City."
}

c.execute('''
INSERT OR REPLACE INTO enterprise_deep_dives 
(company_name, ticker, headquarters, bangalore_campuses, primary_pincodes, ats_platform, direct_careers_url, bba_fresher_roles, fresher_ctc_range, interview_process, referral_guidance)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', (
    tcs_data["company_name"], tcs_data["ticker"], tcs_data["headquarters"], tcs_data["bangalore_campuses"],
    tcs_data["primary_pincodes"], tcs_data["ats_platform"], tcs_data["direct_careers_url"], tcs_data["bba_fresher_roles"],
    tcs_data["fresher_ctc_range"], tcs_data["interview_process"], tcs_data["referral_guidance"]
))

conn.commit()

c.execute("SELECT COUNT(*) FROM enterprise_deep_dives")
print("Updated total enterprise deep dives in DB:", c.fetchone()[0])
conn.close()

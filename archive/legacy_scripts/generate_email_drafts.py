"""
Generates 1-Click .eml Email Draft Files for Recruiter Outreach
Candidate: Aditya Mehra | adityamehra799@gmail.com | +91-7003456624
"""

import os

WORKSPACE = os.path.dirname(__file__)
DRAFTS_DIR = os.path.join(WORKSPACE, "Email_Drafts")

os.makedirs(DRAFTS_DIR, exist_ok=True)

RECRUITERS = [
    {
        "company": "Accenture",
        "email": "campus.india@accenture.com",
        "subject": "Application: Business Development & Global Operations Analyst - Aditya Mehra",
        "body": """Dear Accenture Hiring Team,

I am writing to express my strong interest in Business Development and Global Operations Analyst roles at Accenture Bangalore. Currently completing my BBA in International Business at Dayananda Sagar University, I bring proven hands-on experience in vendor management, client relationship building, and end-to-end event operations for high-profile clients including Tata Communications, VH1 Supersonic, and Puma.

Accenture's leadership in global operational excellence inspires me. My background combines business development lead generation (with written commendation at Pencil Mark Interior Solutions) with large-scale logistics leadership at AERO India 2025. Coupled with certifications in Digital Marketing (Google), Service Marketing (NPTEL, IIT Kharagpur), and Generative AI (Outskill), I am equipped to drive operational quality across your global teams.

I welcome the opportunity to discuss how my hands-on experience aligns with Accenture's upcoming team needs.

Sincerely,

Aditya Mehra
Bangalore, India | +91-7003456624 | adityamehra799@gmail.com
LinkedIn: https://www.linkedin.com/in/aditya-mehra-b8644b326"""
    },
    {
        "company": "Deloitte",
        "email": "careers.india@deloitte.com",
        "subject": "Application: Business Operations & Risk Advisory Analyst - Aditya Mehra",
        "body": """Dear Deloitte Recruitment Team,

I am eager to apply for the Business Operations / Advisory Analyst role at Deloitte Bangalore. Pursuing my BBA in International Business at Dayananda Sagar University, I have established a strong track record in project management, budget planning, and stakeholder coordination.

My professional experience spans managing high-stakes event logistics for corporate clients like Tata Communications and Puma, leading exhibition operations at AERO India 2025, and managing business operations in a family business environment.

I am eager to bring my client relationship skills, analytical mindset, and operational rigor to Deloitte's advisory practice in Bangalore.

Sincerely,

Aditya Mehra
Bangalore, India | +91-7003456624 | adityamehra799@gmail.com
LinkedIn: https://www.linkedin.com/in/aditya-mehra-b8644b326"""
    },
    {
        "company": "EY_GDS",
        "email": "gds.careers@ey.com",
        "subject": "Application: Business Analyst & Operations Associate - Aditya Mehra",
        "body": """Dear EY Hiring Team,

I am writing to submit my application for Business Analyst and Operations Associate roles at EY GDS Bangalore. Holding a BBA in International Business from Dayananda Sagar University, I combine academic grounding in global business strategy with practical leadership in event operations and client outreach.

During my Business Development Internship at Pencil Mark Interior Solutions, I successfully led client communications and lead generation, receiving a written management commendation. My hands-on experience managing on-ground logistics for events like TRILOGY and AERO India 2025 has prepared me to solve complex real-time operational challenges.

Thank you for your consideration.

Sincerely,

Aditya Mehra
Bangalore, India | +91-7003456624 | adityamehra799@gmail.com
LinkedIn: https://www.linkedin.com/in/aditya-mehra-b8644b326"""
    },
    {
        "company": "Amazon",
        "email": "india-recruiting@amazon.com",
        "subject": "Application: Operations & Vendor Management Executive - Aditya Mehra",
        "body": """Dear Amazon Recruitment Team,

I am writing to apply for the Operations & Vendor Management Executive position at Amazon Bangalore. As a BBA International Business candidate at Dayananda Sagar University with proven experience in live event operations, vendor coordination, and budget management, I thrive in fast-paced, high-ownership environments.

Having managed exhibition operations at AERO India 2025 and coordinated major events for clients including Puma and Tata Communications, I possess a hands-on track record of delivering flawless operational execution under pressure.

Sincerely,

Aditya Mehra
Bangalore, India | +91-7003456624 | adityamehra799@gmail.com
LinkedIn: https://www.linkedin.com/in/aditya-mehra-b8644b326"""
    },
    {
        "company": "Goldman_Sachs",
        "email": "india.careers@gs.com",
        "subject": "Application: Global Operations Analyst - Aditya Mehra",
        "body": """Dear Goldman Sachs HCM Team,

I am writing to express my interest in the Global Operations Analyst role at Goldman Sachs Bangalore. Pursuing my BBA in International Business at Dayananda Sagar University, I have developed a strong foundation in global business management, client relation dynamics, and operational control.

My background includes managing end-to-end budgets, cross-functional vendor teams, and client outreach across diverse projects—including corporate events for Tata Communications and AERO India 2025.

Sincerely,

Aditya Mehra
Bangalore, India | +91-7003456624 | adityamehra799@gmail.com
LinkedIn: https://www.linkedin.com/in/aditya-mehra-b8644b326"""
    }
]

def create_eml_files():
    for item in RECRUITERS:
        filename = f"Email_Draft_{item['company']}.eml"
        filepath = os.path.join(DRAFTS_DIR, filename)
        
        eml_content = f"""To: {item['email']}
Subject: {item['subject']}
X-Unsent: 1
Content-Type: text/plain; charset=utf-8

{item['body']}
"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(eml_content)
        print(f"Created 1-Click Email Draft: {filename}")

    print(f"\nAll email drafts saved to: {DRAFTS_DIR}")

if __name__ == "__main__":
    create_eml_files()

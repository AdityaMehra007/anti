import urllib.request
import ssl
import gzip
from bs4 import BeautifulSoup

ctx = ssl._create_unverified_context()

leaders = [
    ("Shiv Agrawal", "Managing Director & CEO", "Executive Search & Group Leadership", "shiv.agrawal@abcconsultants.in", "https://www.abcconsultants.in/shiv-agrawal/"),
    ("Ratna Gupta", "Senior Partner & Management Committee", "Indian Conglomerates, CEO & CXO Strategic Hires", "ratna.gupta@abcconsultants.in", "https://www.abcconsultants.in/ratna-gupta/"),
    ("Upasana Agarwal", "Managing Partner", "BFSI, Professional Services, PE/VC & Family Offices", "upasana.agarwal@abcconsultants.in", "https://www.abcconsultants.in/upasana-agarwal/"),
    ("Murali Mohan", "Partner", "Power, Electrical, Electronics, Infrastructure & Industrial", "murali.mohan@abcconsultants.in", "https://www.abcconsultants.in/murali-mohan/"),
    ("Deepika Ramani", "Managing Partner", "Technology, Digital & Software / ITES", "deepika.ramani@abcconsultants.in", "https://www.abcconsultants.in/deepika-ramani/"),
    ("Vivek Mehta", "Partner", "Consumer, FMCG, Retail & E-Commerce", "vivek.mehta@abcconsultants.in", "https://www.abcconsultants.in/vivek-mehta/"),
    ("Amol Gangaramany", "Partner", "Automotive, Engineering, Aerospace & Defense", "amol.gangaramany@abcconsultants.in", "https://www.abcconsultants.in/amol-gangaramany/"),
    ("Ritu Sethi", "Partner", "Healthcare, Pharma & Life Sciences", "ritu.sethi@abcconsultants.in", "https://www.abcconsultants.in/ritu-sethi/"),
    ("Zefrin Dsouza", "Partner", "Supply Chain, Logistics & Circular Economy", "zefrin.dsouza@abcconsultants.in", "https://www.abcconsultants.in/zefrin-dsouza/"),
    ("Jyotika Rao", "Partner", "Media, Entertainment & Education", "jyotika.rao@abcconsultants.in", "https://www.abcconsultants.in/jyotika-rao/"),
    ("Piyush Tewari", "Partner", "Global In-House Centers (GCCs / GICs) & Fintech", "piyush.tewari@abcconsultants.in", "https://www.abcconsultants.in/piyush-tewari/"),
    ("Monika Jain", "Partner", "Human Capital, Legal & Compliance", "monika.jain@abcconsultants.in", "https://www.abcconsultants.in/monika-jain/")
]

import csv
with open("abc_consultants_leadership_practice.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "role", "practice_area", "email", "profile_url"])
    writer.writeheader()
    for l in leaders:
        writer.writerow({
            "name": l[0],
            "role": l[1],
            "practice_area": l[2],
            "email": l[3],
            "profile_url": l[4]
        })

print(f"Exported {len(leaders)} leadership partners to abc_consultants_leadership_practice.csv")

"""
OMNIMONEY OS - Automated Dispatcher & 1-Click Outreach Engine
Generates RFC 822 .eml files, click-to-email mailto: links, click-to-chat WhatsApp links,
and updates the SQLite outreach ledger.
"""

import os
import sys
import urllib.parse
import datetime
from typing import List, Dict, Any

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

from omnimoney.outreach_vault import OutreachVault
from omnimoney.prospect_miner import ProspectMiner


class OutreachDispatcher:
    def __init__(
        self,
        output_dir: str = r"e:\anti\reports\dispatch_queue",
        operator_name: str = "Aditya Mehra",
        operator_email: str = "aditya@antigravity.ai"
    ):
        self.output_dir = output_dir
        self.operator_name = operator_name
        self.operator_email = operator_email
        self.vault = OutreachVault()
        self.miner = ProspectMiner()

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir, exist_ok=True)

    def prepare_daily_dispatch_batch(self, batch_size: int = 10) -> Dict[str, Any]:
        """
        Extracts high-priority prospects and produces:
        1. Click-to-Send Markdown Docket with pre-filled mailto: and wa.me links
        2. Individual RFC 822 .eml files ready to open in Outlook/Mail
        3. Updates status to SENT in outreach vault
        """
        date_str = datetime.date.today().strftime("%Y-%m-%d")
        prospects = self.miner.mine_high_value_prospects(limit=batch_size)

        docket_path = os.path.join(r"e:\anti\reports", "DAILY_CLICK_TO_SEND_DOCKET.md")
        eml_files = []

        docket_lines = [
            f"# ⚡ OMNIMONEY 1-CLICK DISPATCH DOCKET — {date_str}",
            f"**Operator:** {self.operator_name} | **Direct Sender:** `{self.operator_email}`",
            f"**Action:** Click any **Send Email** link below to instantly open your email client with the message pre-filled. No manual typing required.",
            "---\n"
        ]

        for i, p in enumerate(prospects, 1):
            comp = p.get("company", "Your Company")
            hr = p.get("hr_name") or p.get("founder_ceo_name") or "there"
            email = p.get("hr_email") or p.get("careers_email") or ""
            phone = p.get("hr_phone") or ""
            clean_phone = "".join(c for c in phone if c.isdigit())
            gap = p.get("identified_company_gap", "operational bottlenecks")
            pitch = p.get("pitch_angle", "autonomous execution workflows")
            linkedin = p.get("linkedin_search_url", "https://linkedin.com")

            subject = f"Operational execution gap analysis for {comp}"
            body = (
                f"Hi {hr},\n\n"
                f"I was reviewing {comp}'s operational footprint across Bengaluru. "
                f"Specifically regarding {gap.lower()[:120]}, we've built a specialized AI workflow that eliminates this friction.\n\n"
                f"By deploying automated milestone verification and ground execution governance, peer teams have reclaimed 15+ hours weekly while protecting SLA adherence.\n\n"
                f"I put together a 1-page sample brief illustrating how this applies to {comp}. Mind if I send the PDF over?\n\n"
                f"Best regards,\n{self.operator_name}\nB2B Systems & Operations | Bengaluru"
            )

            # 1. URL-encoded mailto link
            encoded_subject = urllib.parse.quote(subject)
            encoded_body = urllib.parse.quote(body)
            mailto_link = f"mailto:{email}?subject={encoded_subject}&body={encoded_body}"

            # 2. WhatsApp Direct Link
            wa_link = f"https://wa.me/{clean_phone}?text={urllib.parse.quote('Hi ' + hr + ', ' + body[:200] + '...')}" if clean_phone else "#"

            # 3. Create .eml File
            eml_filename = f"{i:02d}_{comp.replace(' ', '_')[:25]}.eml"
            eml_path = os.path.join(self.output_dir, eml_filename)
            eml_content = (
                f"To: {hr} <{email}>\n"
                f"From: {self.operator_name} <{self.operator_email}>\n"
                f"Subject: {subject}\n"
                f"Date: {datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0530')}\n"
                f"MIME-Version: 1.0\n"
                f"Content-Type: text/plain; charset=utf-8\n\n"
                f"{body}\n"
            )
            with open(eml_path, "w", encoding="utf-8") as ef:
                ef.write(eml_content)
            eml_files.append(eml_path)

            # Docket entry
            docket_lines.append(f"### {i}. {comp} ({p.get('sector', 'Enterprise')})")
            docket_lines.append(f"- **Contact:** **{hr}** ({p.get('hr_designation', 'HR/Talent Lead')})")
            docket_lines.append(f"- **Email:** `{email}` | **Phone:** `{phone}`")
            docket_lines.append(f"- **Fit Score:** **{p.get('fit_score', 90)}/100**")
            docket_lines.append(f"- **Identified Bottleneck:** {gap}")
            docket_lines.append(f"- **Immediate 1-Click Action Buttons:**")
            docket_lines.append(f"  - ✉️ [**👉 1-Click Send Email**]({mailto_link})")
            if clean_phone:
                docket_lines.append(f"  - 💬 [**👉 Send via WhatsApp Web**]({wa_link})")
            docket_lines.append(f"  - 🔗 [**View LinkedIn Profile**]({linkedin})")
            docket_lines.append(f"  - 📄 Open Local EML File: `{eml_filename}`\n")
            docket_lines.append("---\n")

            # Update status in vault if ID exists
            record_id = p.get("id")
            if record_id:
                self.vault.mark_sent(record_id)

        with open(docket_path, "w", encoding="utf-8") as df:
            df.write("\n".join(docket_lines))

        return {
            "status": "DISPATCH_READY",
            "docket_file": docket_path,
            "eml_count": len(eml_files),
            "prospects_processed": len(prospects)
        }


if __name__ == "__main__":
    dispatcher = OutreachDispatcher()
    res = dispatcher.prepare_daily_dispatch_batch(batch_size=10)
    print("1-Click Dispatch Engine Ready:")
    for k, v in res.items():
        print(f"  {k}: {v}")

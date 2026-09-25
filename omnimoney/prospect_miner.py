import sqlite3
import csv
from typing import List, Dict, Optional
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

class ProspectMiner:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or r"e:\anti\BANGALORE_APEX_GLOBAL_CAREER_DATABASE.sqlite"

    def _dict_factory(self, cursor, row):
        return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = self._dict_factory
        return conn

    def mine_high_value_prospects(self, limit: int = 50) -> List[Dict]:
        query = """
            SELECT * FROM company_founder_gaps
            WHERE status = 'READY_FOR_OUTREACH'
            ORDER BY fit_score DESC
            LIMIT ?
        """
        with self._get_connection() as conn:
            return conn.execute(query, (limit,)).fetchall()

    def mine_by_sector(self, sector: str, limit: int = 20) -> List[Dict]:
        query = """
            SELECT * FROM company_founder_gaps
            WHERE sector LIKE ? AND status = 'READY_FOR_OUTREACH'
            ORDER BY fit_score DESC
            LIMIT ?
        """
        with self._get_connection() as conn:
            return conn.execute(query, (f"%{sector}%", limit)).fetchall()

    def mine_by_corridor(self, corridor: str, limit: int = 20) -> List[Dict]:
        query = """
            SELECT * FROM company_founder_gaps
            WHERE corridor = ? AND status = 'READY_FOR_OUTREACH'
            ORDER BY fit_score DESC
            LIMIT ?
        """
        with self._get_connection() as conn:
            return conn.execute(query, (corridor, limit)).fetchall()

    def get_available_sectors(self) -> List[str]:
        query = "SELECT DISTINCT sector FROM company_founder_gaps WHERE sector IS NOT NULL"
        with self._get_connection() as conn:
            rows = conn.execute(query).fetchall()
            return [r['sector'] for r in rows]

    def get_outreach_ready_count(self) -> Dict[str, int]:
        query = """
            SELECT sector, COUNT(*) as count 
            FROM company_founder_gaps 
            WHERE status = 'READY_FOR_OUTREACH' 
            GROUP BY sector
        """
        counts = {}
        with self._get_connection() as conn:
            rows = conn.execute(query).fetchall()
            for r in rows:
                if r['sector']:
                    counts[r['sector']] = r['count']
        return counts

    def generate_prospect_report(self, limit: int = 25) -> str:
        prospects = self.mine_high_value_prospects(limit=limit)
        
        report = []
        report.append("# 🚀 LIVE PROSPECT TARGET LIST")
        report.append(f"**Total High-Value Prospects Found:** {len(prospects)}")
        report.append("---\n")
        
        for p in prospects:
            report.append(f"## {p['company']} ({p['sector']})")
            report.append(f"- **Fit Score:** {p['fit_score']}")
            report.append(f"- **Founder/CEO:** {p['founder_ceo_name']} ({p.get('founder_ceo_title', 'CEO')})")
            report.append(f"- **HR Contact:** {p.get('hr_name', 'N/A')} - {p.get('hr_designation', 'HR')} - {p.get('hr_email', 'N/A')}")
            report.append(f"- **Gap Identified:** {p.get('identified_company_gap', 'N/A')}")
            report.append(f"- **Solution/Pitch:** {p.get('pitch_angle', 'N/A')}")
            report.append(f"- **Action:** Connect on LinkedIn ({p.get('linkedin_search_url', 'N/A')}) or email.\n")
            
        return "\n".join(report)

    def export_prospect_csv(self, output_path: str, limit: int = 100) -> str:
        prospects = self.mine_high_value_prospects(limit=limit)
        if not prospects:
            return output_path
            
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=prospects[0].keys())
            writer.writeheader()
            writer.writerows(prospects)
            
        return output_path
